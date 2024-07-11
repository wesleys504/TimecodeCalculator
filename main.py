def timecode_to_frames(timecode, frame_rate, drop_frame=False):
    """Convert a timecode string to the total number of frames, handling drop frame if necessary."""
    try:
        parts = list(map(int, timecode.split(':')))
        if len(parts) == 3:
            minutes, seconds, frames = parts
            hours = 0
        elif len(parts) == 4:
            hours, minutes, seconds, frames = parts
        else:
            raise ValueError("Invalid timecode format. Please use HH:MM:SS:FF or MM:SS:FF.")

        if drop_frame and frame_rate == 30:
            # Drop frame timecode calculation
            total_minutes = hours * 60 + minutes
            drop_frames = 2 * (total_minutes - total_minutes // 10)
            total_frames = ((hours * 3600 + minutes * 60 + seconds) * frame_rate + frames) - drop_frames
        else:
            total_frames = (hours * 3600 + minutes * 60 + seconds) * frame_rate + frames
        return total_frames
    except ValueError:
        raise ValueError("Invalid timecode format. Please use HH:MM:SS:FF or MM:SS:FF.")

def frames_to_timecode(total_frames, frame_rate, drop_frame=False):
    """Convert the total number of frames to a timecode string, handling drop frame if necessary."""
    if drop_frame and frame_rate == 30:
        frames_per_hour = 107892  # 30*3600 - 108
        frames_per_10_minutes = 17982  # 30*600 - 18
        frames_per_minute = 1798  # 30*60 - 2

        hours = total_frames // frames_per_hour
        total_frames %= frames_per_hour
        minutes = total_frames // frames_per_10_minutes * 10
        total_frames %= frames_per_10_minutes

        while total_frames >= frames_per_minute:
            total_frames -= frames_per_minute
            minutes += 1

        seconds = total_frames // frame_rate
        frames = total_frames % frame_rate
    else:
        frames = total_frames % frame_rate
        total_seconds = total_frames // frame_rate
        seconds = total_seconds % 60
        total_minutes = total_seconds // 60
        minutes = total_minutes % 60
        hours = total_minutes // 60

    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

def calculate_overrun(current_total_frames, target_frame_rate, target_duration, target_drop_frame=False):
    """Calculate how much over or under the target duration the current sequence is."""
    target_total_frames = timecode_to_frames(target_duration, target_frame_rate, target_drop_frame)

    overrun_frames = current_total_frames - target_total_frames
    overrun_timecode = frames_to_timecode(abs(overrun_frames), target_frame_rate, target_drop_frame)

    if overrun_frames > 0:
        return f"Over by {overrun_timecode}"
    elif overrun_frames < 0:
        return f"Under by {overrun_timecode}"
    else:
        return "Exact duration"

def get_input(prompt, input_type=str):
    """Get input from the user and handle simple validation."""
    while True:
        try:
            value = input_type(input(prompt))
            if input_type == str and not value:
                raise ValueError("This field cannot be empty.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def get_frame_rate(prompt):
    """Get a valid frame rate from the user."""
    while True:
        try:
            frame_rate = int(input(prompt))
            if frame_rate <= 0:
                raise ValueError("Frame rate must be a positive integer.")
            return frame_rate
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a positive integer for the frame rate.")

def get_drop_frame_option(prompt):
    """Get drop frame option from the user."""
    while True:
        try:
            response = input(prompt).strip().lower()
            if response in ['yes', 'no']:
                return response == 'yes'
            else:
                raise ValueError("Please enter 'yes' or 'no'.")
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def get_timecode(prompt):
    """Get a valid timecode from the user."""
    while True:
        try:
            timecode = input(prompt).strip()
            # Attempt to parse the timecode to ensure it is valid
            timecode_to_frames(timecode, 30)  # Using a sample frame rate to validate
            return timecode
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter the timecode in HH:MM:SS:FF or MM:SS:FF format.")

def main():
    print("Timecode Calculator/Converter")

    type_of_content = get_input("Is this a Feature Film or a TV Show? (feature/tv): ").strip().lower()

    if type_of_content == "feature":
        current_frame_rate = get_frame_rate("Enter the current frame rate (e.g., 24, 25, 30): ")
        current_drop_frame = get_drop_frame_option("Is the current timecode drop frame? (yes/no): ")
        current_timecode = get_timecode("Enter the current sequence timecode (HH:MM:SS:FF or MM:SS:FF): ")
        current_total_frames = timecode_to_frames(current_timecode, current_frame_rate, current_drop_frame)

    elif type_of_content == "tv":
        num_acts = get_input("How many acts are there? ", int)
        current_frame_rate = get_frame_rate("Enter the current frame rate (e.g., 24, 25, 30): ")
        current_drop_frame = get_drop_frame_option("Is the current timecode drop frame? (yes/no): ")
        current_total_frames = 0

        for act in range(num_acts):
            act_timecode = get_timecode(f"Enter the timecode for act {act+1} (HH:MM:SS:FF or MM:SS:FF): ")
            current_total_frames += timecode_to_frames(act_timecode, current_frame_rate, current_drop_frame)

        trt_timecode = frames_to_timecode(current_total_frames, current_frame_rate, current_drop_frame)
        print(f"Total Run Time (TRT) of all acts: {trt_timecode}")

    target_frame_rate = get_frame_rate("Enter the delivery frame rate (e.g., 24, 25, 30): ")
    target_drop_frame = get_drop_frame_option("Is the delivery timecode drop frame? (yes/no): ")
    target_duration = get_timecode("Enter the target duration timecode (HH:MM:SS:FF or MM:SS:FF): ")

    try:
        overrun = calculate_overrun(current_total_frames, target_frame_rate, target_duration, target_drop_frame)
        print(overrun)
    except ValueError as e:
        print(f"Error: {e}. Please try again.")

if __name__ == "__main__":
    main()
