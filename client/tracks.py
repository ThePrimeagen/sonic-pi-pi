from typing import List 
from dataclasses import dataclass

TrackPositions = List[int]
TrackNames = List[str]

@dataclass
class TrackState:
    tracks: TrackPositions
    track_names: TrackNames

class TrackList:
    tracks: TrackPositions
    track_names: TrackNames

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        # This is 4 whole notes
        # TODO: This is 16 whole notes
        self.tracks = [
            [0] * 32,
            [0] * 16,
            [0] * 16,
        ]

        self.track_names = [
            ":drum_cymbal_closed",
            ":drum_bass_soft",
            ":drum_snare_soft",
        ]

    def get_state(self) -> TrackState:
        return TrackState(tracks=self.tracks, track_names=self.track_names)

    def get_music(self):
        content = f"""
use_bpm 120

            """
        for i, x in enumerate(self.tracks):
            content += f"""
track{i} = [{",".join(list(map(str, x)))}]
track{i}_name = {self.track_names[i]}
track{i}_sleep = {0.125 if len(self.tracks[i]) == 32 else 0.25}
    """

        content += """
live_loop :pulse do
    sleep 4
end

define :run_p do |name, pattern, sample_name, sleep_rate|
    sync :pulse
    live_loop name do
        pattern.each do |p|
            sample sample_name, amp: p/9.0
            sleep sleep_rate
        end
    end
end
    """
        for i, x in enumerate(self.tracks):
            content += f"run_p :track{i}, track{i}, track{i}_name, track{i}_sleep\n"

        return content

    def run_command(self, user, cmd):
        try:
            command, track, position  = cmd.split(" ")
            if not command == "!play" and not command == "!stop":
                return

            # ignore this track item
            track = int(track)

            if len(self.tracks) <= track or track < 0:
                print(f"{user} Invalid Track {track}", flush=True)
                return

            position = int(position)

            t = self.tracks[track]
            if len(t) <= position or position < 0:
                print(f"{user} Invalid Position {position}", flush=True)
                return

            play = command == "!play"

            t[position] = 5 if play else 0
            return True

        except Exception as e:
            print(f"Nice try guy {user} {str(e)}")

        return False

