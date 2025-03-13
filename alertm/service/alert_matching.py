import os
from typing import List, Literal, Optional, Tuple

import torch
from config import embedding_config
from loguru import logger
from schema.request import Alert, Event
from schema.response import AlertResp, MatchingAlert
from sentence_transformers import SentenceTransformer, SimilarityFunction
from utils.path import APP_PATH


class AlertMatching:
    def __init__(
            self,
            model_name: Optional[str] = None,
            device: Optional[Literal["cuda", "cpu"]] = None,
            batch_size: Optional[int] = None,
    ):
        model_name = model_name or embedding_config.model
        device = device or embedding_config.device
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.batch_size = batch_size or embedding_config.batch_size

        logger.info(f"Model is running on {device}")
        self.embedder = SentenceTransformer(model_name_or_path=model_name,
                                            device=device,
                                            trust_remote_code=True,
                                            similarity_fn_name=SimilarityFunction.COSINE,
                                            cache_folder=os.path.join(APP_PATH, "cache")
                                            )

    def calculate_similarity(self, event: str, alerts: List[str]) -> List[Tuple[int, float]]:
        docs = [event] + alerts
        corpus_embeddings = self.embedder.encode(sentences=docs,
                                                 batch_size=embedding_config.batch_size,
                                                 normalize_embeddings=True)
        event_embedding = corpus_embeddings[0]
        alerts_embedding = corpus_embeddings[1:]
        similarity_scores = self.embedder.similarity(event_embedding, alerts_embedding)[0]
        print("similarity_scores: ", similarity_scores)

        # Get indices where score > 0.5
        indices = torch.where(similarity_scores > embedding_config.threshold)[0]
        # Get the corresponding scores
        scores = similarity_scores[indices]
        scores = scores.tolist()
        indices = indices.tolist()
        return [(index, round(score, 3)) for index, score in zip(indices, scores)]

    @staticmethod
    def filter(event: Event, alerts: List[Alert]) -> List[Alert]:
        """Exact match based on topic and environment"""
        return [
            alert for alert in alerts
            if alert.topic == event.topic and alert.environment == event.environment
               and alert.resource == event.resource and alert.service == event.service
        ]

    def match_alert(self, event: Event, alerts: List[Alert]) -> AlertResp:
        """Return alerts that match with event"""
        alerts_filtered = self.filter(event, alerts)

        alerts_str = [_alert.description for _alert in alerts_filtered]
        alerts_similarity = self.calculate_similarity(event=event.content, alerts=alerts_str)

        alerts_matched = [MatchingAlert(alert_id=alerts_filtered[idx].id, confidence=score)
                          for idx, score in alerts_similarity]

        return AlertResp(
            message="success", alerts=alerts_matched
        )
