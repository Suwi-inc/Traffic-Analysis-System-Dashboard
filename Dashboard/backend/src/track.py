from deep_sort_realtime.deepsort_tracker import DeepSort


class Tracker:
    def __init__(self):
        self.object_tracker = DeepSort(
            max_age=20,
            n_init=2,
            nms_max_overlap=0.3,
            max_cosine_distance=0.8,
            nn_budget=None,
            override_track_class=None,
            embedder="mobilenet",
            half=True,  # Half-precision floating point (FP16) for GPU
            bgr=True,
            embedder_model_name=None,
            embedder_wts=None,
            polygon=False,
            today=None,
        )

    def track(self, detections, frame, label):
        tracks = self.object_tracker.update_tracks(
            detections, frame=frame, others=label
        )

        tracking_data = []
        for i, track in enumerate(tracks):
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            ltrb = track.to_ltrb()
            detection_label = track.get_det_supplementary()
            tracking_data.append((track_id, ltrb, detection_label))

        return tracking_data
