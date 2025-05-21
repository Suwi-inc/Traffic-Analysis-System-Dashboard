from collections import Counter


def calculate_lane_occupancy(lane_occupancy_frames, total_frames):
    """
    Calculate lane occupancy rate as a percentage. Shows is the percentage
    of time a given lane is occupied by one or more vehicles over a specified observation period.
    Value of >= 0.7 - high occupancy
    value of >= 0.4 - moderate occupancy
    value of < 0.4 - low occupancy
    Args:
        lane_occupancy_frames (dict): {lane_id: number_of_frames_occupied}
        total_frames (int): Total number of frames observed

    Returns:
        dict: {lane_id: occupancy_rate_percentage}
    """
    occupancy_rates = {}
    for lane_id, occupied_frames in lane_occupancy_frames.items():
        occupancy = (occupied_frames / total_frames) * 100 if total_frames > 0 else 0
        occupancy_rates[lane_id] = round(occupancy, 2)
    return occupancy_rates


def vehicle_type_distribution(vehicle_labels_per_lane):
    """
    Calculate vehicle type distribution based on vehicle labels.

    Args:
        vehicle_labels_per_lane (dict): {lane_id: [label1, label2, ...]}

    Returns:
        dict: {lane_id: {'car': count, 'truck': count, ...}}
    """
    distribution = {}
    for lane_id, labels in vehicle_labels_per_lane.items():
        count = Counter(labels)
        distribution[lane_id] = dict(count)

    return distribution
