def center_blur_bound(closing_speed, opening_speed, exposure_seconds):
    return (closing_speed + opening_speed) * exposure_seconds / 8
