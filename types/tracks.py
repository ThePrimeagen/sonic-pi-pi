
TrackPositions = List[int]
TrackNames = List[str]

@dataclass
class TrackState:
    tracks: TrackPositions
    track_names: TrackNames

