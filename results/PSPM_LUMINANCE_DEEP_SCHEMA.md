# PsPM luminance deep MATLAB schema

## AOB_UW_pupil_01_sn2.mat

infos: type=mat_struct shape=None dtype=None
  importdate: type=str shape=None dtype=None
    value='16-Aug-2023'
  source: type=mat_struct shape=None dtype=None
    channel: type=ndarray shape=(6,) dtype=object
      [0]: type=str shape=None dtype=None
        value='Column 01'
      [1]: type=str shape=None dtype=None
        value='Column 02'
      [2]: type=str shape=None dtype=None
        value='Column 03'
      [3]: type=str shape=None dtype=None
        value='Column 04'
      [4]: type=str shape=None dtype=None
        value='Column 05'
      [5]: type=str shape=None dtype=None
        value='Column 06'
    chan_stats: type=ndarray shape=(6,) dtype=object
      [0]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.2231975075135734
      [1]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.2034020725832614
      [2]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.2231975075135734
      [3]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.2231975075135734
      [4]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.2034020725832614
      [5]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.2034020725832614
    gaze_coords: type=mat_struct shape=None dtype=None
      xmin: type=int shape=None dtype=None
        value=0
      ymin: type=int shape=None dtype=None
        value=0
      xmax: type=int shape=None dtype=None
        value=1023
      ymax: type=int shape=None dtype=None
        value=767
    elcl_proc: type=str shape=None dtype=None
      value='ellipse'
    eyesObserved: type=str shape=None dtype=None
      value='lr'
    best_eye: type=str shape=None dtype=None
      value='r'
    type: type=str shape=None dtype=None
      value='Eyelink 1000 (.asc)'
  duration: type=float shape=None dtype=None
    value=288.106
  durationinfo: type=str shape=None dtype=None
    value='Recording duration in seconds'
data: type=ndarray shape=(7,) dtype=object
  [0]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='pupil_l'
      sr: type=int shape=None dtype=None
        value=500
      units: type=str shape=None dtype=None
        value='mm'
    data: type=ndarray shape=(144053,) dtype=float64
      sample=[3.1084148547857144, 3.1113291758571426, 3.1136606327142857, 3.112494904285714, 3.112494904285714, 3.112494904285714, 3.1130777684999997, 3.1148263611428573, 3.1130777684999997, 3.1119120400714286, 3.1130777684999997, 3.1136606327142857]
      min=2.2026438657857144 max=4.238588566285714 mean=3.01035039498194
  [1]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='pupil_r'
      sr: type=int shape=None dtype=None
        value=500
      units: type=str shape=None dtype=None
        value='mm'
    data: type=ndarray shape=(144053,) dtype=float64
      sample=[3.0314767785, 3.029728185857143, 3.0303110500714285, 3.0285624574285714, 3.029145321642857, 3.0320596427142856, 3.032642506928571, 3.0320596427142856, 3.0285624574285714, 3.027396729, 3.030893914285714, 3.033225371142857]
      min=2.1204600115714287 max=4.112689896 mean=2.9323710312413724
  [2]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='gaze_x_l'
      sr: type=int shape=None dtype=None
        value=500
      range: type=ndarray shape=(2,) dtype=uint16
        values=[0, 1023]
      units: type=str shape=None dtype=None
        value='pixel'
    data: type=ndarray shape=(144053,) dtype=float64
      sample=[580.9, 580.5, 580.2, 580.5, 580.7, 581.1, 580.2, 579.1, 578.7, 579.4, 580.7, 581.6]
      min=12.2 max=741.2 mean=508.9978578955551
  [3]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='gaze_y_l'
      sr: type=int shape=None dtype=None
        value=500
      range: type=ndarray shape=(2,) dtype=uint16
        values=[0, 767]
      units: type=str shape=None dtype=None
        value='pixel'
    data: type=ndarray shape=(144053,) dtype=float64
      sample=[485.0, 484.1, 484.0, 485.2, 484.9, 484.4, 484.7, 484.8, 485.0, 484.4, 483.3, 483.8]
      min=39.3 max=1500.0 mean=412.08070378496035
  [4]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='gaze_x_r'
      sr: type=int shape=None dtype=None
        value=500
      range: type=ndarray shape=(2,) dtype=uint16
        values=[0, 1023]
      units: type=str shape=None dtype=None
        value='pixel'
    data: type=ndarray shape=(144053,) dtype=float64
      sample=[572.7, 572.5, 572.6, 572.7, 573.0, 573.2, 573.3, 573.5, 573.5, 573.6, 573.6, 573.7]
      min=-11.7 max=716.6 mean=496.7649666049183
  [5]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='gaze_y_r'
      sr: type=int shape=None dtype=None
        value=500
      range: type=ndarray shape=(2,) dtype=uint16
        values=[0, 767]
      units: type=str shape=None dtype=None
        value='pixel'
    data: type=ndarray shape=(144053,) dtype=float64
      sample=[473.5, 474.5, 475.3, 475.1, 475.2, 475.3, 474.9, 474.4, 474.5, 474.6, 474.4, 473.3]
      min=52.8 max=1529.3 mean=406.64783059431346
  [6]: type=mat_struct shape=None dtype=None
    data: type=ndarray shape=(49,) dtype=float64
      sample=[3.0, 48.008, 53.01200000000001, 58.014, 63.016, 68.018, 73.02000000000001, 78.02199999999999, 83.024, 88.02600000000001, 93.02800000000002, 98.03]
      min=3.0 max=283.106 mean=162.24081632653065
    markerinfo: type=mat_struct shape=None dtype=None
      name: type=ndarray shape=(49,) dtype=object
        [0]: type=str shape=None dtype=None
          value='M600'
        [1]: type=str shape=None dtype=None
          value='M400'
        [2]: type=str shape=None dtype=None
          value='M600'
        [3]: type=str shape=None dtype=None
          value='M100'
        [4]: type=str shape=None dtype=None
          value='M600'
        [5]: type=str shape=None dtype=None
          value='M100'
        [6]: type=str shape=None dtype=None
          value='M600'
        [7]: type=str shape=None dtype=None
          value='M200'
        [8]: type=str shape=None dtype=None
          value='M600'
        [9]: type=str shape=None dtype=None
          value='M300'
        [10]: type=str shape=None dtype=None
          value='M600'
        [11]: type=str shape=None dtype=None
          value='M100'
      value: type=ndarray shape=(49,) dtype=uint8
        sample=[5, 4, 5, 1, 5, 1, 5, 2, 5, 3, 5, 1]
        min=1.0 max=5.0 mean=3.7755102040816326
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='marker'
      units: type=str shape=None dtype=None
        value='events'
      sr: type=int shape=None dtype=None
        value=1

## AOB_UW_cogent_01_sn2.mat

subject: type=mat_struct shape=None dtype=None
  age: type=int shape=None dtype=None
    value=37
  gender: type=str shape=None dtype=None
    value='f'
  screen_dist: type=int shape=None dtype=None
    value=590
  track_dist: type=int shape=None dtype=None
    value=465
  screen_width: type=float shape=None dtype=None
    value=396.68135519705936
  screen_height: type=float shape=None dtype=None
    value=317.34508415764753
data: type=ndarray shape=(49, 2) dtype=float64
  sample=[1.0, 9.0, 2.0, 1.0, 3.0, 9.0, 4.0, 0.0, 5.0, 9.0, 6.0, 0.0]
  min=0.0 max=49.0 mean=14.918367346938776
dataKey: type=ndarray shape=(2,) dtype=object
  [0]: type=mat_struct shape=None dtype=None
    column_type: type=str shape=None dtype=None
      value='trial_index'
    column_index: type=int shape=None dtype=None
      value=1
    column_description: type=str shape=None dtype=None
      value='1. Trial index'
  [1]: type=mat_struct shape=None dtype=None
    column_type: type=str shape=None dtype=None
      value='stimulus_type'
    column_index: type=int shape=None dtype=None
      value=2
    column_description: type=str shape=None dtype=None
      value='2. Stimulus type (9: fixation cross; otherwise: RGB values of displayed disc from 0 (black) to 1 (white))'

## AOB_UW_pupil_01_sn1.mat

infos: type=mat_struct shape=None dtype=None
  importdate: type=str shape=None dtype=None
    value='16-Aug-2023'
  source: type=mat_struct shape=None dtype=None
    channel: type=ndarray shape=(6,) dtype=object
      [0]: type=str shape=None dtype=None
        value='Column 01'
      [1]: type=str shape=None dtype=None
        value='Column 02'
      [2]: type=str shape=None dtype=None
        value='Column 03'
      [3]: type=str shape=None dtype=None
        value='Column 04'
      [4]: type=str shape=None dtype=None
        value='Column 05'
      [5]: type=str shape=None dtype=None
        value='Column 06'
    chan_stats: type=ndarray shape=(6,) dtype=object
      [0]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.26920090271542624
      [1]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.22791137858234853
      [2]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.2692049471393789
      [3]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.2692049471393789
      [4]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.22791542300630122
      [5]: type=mat_struct shape=None dtype=None
        nan_ratio: type=float shape=None dtype=None
          value=0.22791542300630122
    gaze_coords: type=mat_struct shape=None dtype=None
      xmin: type=int shape=None dtype=None
        value=0
      ymin: type=int shape=None dtype=None
        value=0
      xmax: type=int shape=None dtype=None
        value=1023
      ymax: type=int shape=None dtype=None
        value=767
    elcl_proc: type=str shape=None dtype=None
      value='ellipse'
    eyesObserved: type=str shape=None dtype=None
      value='lr'
    best_eye: type=str shape=None dtype=None
      value='r'
    type: type=str shape=None dtype=None
      value='Eyelink 1000 (.asc)'
  duration: type=float shape=None dtype=None
    value=406.016
  durationinfo: type=str shape=None dtype=None
    value='Recording duration in seconds'
data: type=ndarray shape=(7,) dtype=object
  [0]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='pupil_l'
      sr: type=int shape=None dtype=None
        value=500
      units: type=str shape=None dtype=None
        value='mm'
    data: type=ndarray shape=(203008,) dtype=float64
      sample=[3.498351014142857, 3.4977681499285715, 3.494853828857143, 3.4913566435714287, 3.489608050928571, 3.487859458285714, 3.486110865642857, 3.484362273, 3.4808650877142857, 3.4756193097857144, 3.4732878529285713, 3.472704988714286]
      min=2.4497782926428573 max=3.9407449527857144 mean=3.063517957419411
  [1]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='pupil_r'
      sr: type=int shape=None dtype=None
        value=500
      units: type=str shape=None dtype=None
        value='mm'
    data: type=ndarray shape=(203008,) dtype=float64
      sample=[3.4604648402142857, 3.4633791612857143, 3.4639620255, 3.4616305686428572, 3.4581333833571426, 3.4558019265, 3.4558019265, 3.4563847907142855, 3.4558019265, 3.454053333857143, 3.454053333857143, 3.453470469642857]
      min=2.302896510642857 max=3.772297194857143 mean=2.9503322289264586
  [2]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='gaze_x_l'
      sr: type=int shape=None dtype=None
        value=500
      range: type=ndarray shape=(2,) dtype=uint16
        values=[0, 1023]
      units: type=str shape=None dtype=None
        value='pixel'
    data: type=ndarray shape=(203008,) dtype=float64
      sample=[486.9, 486.9, 486.8, 487.0, 487.2, 487.2, 487.5, 487.7, 487.4, 487.0, 486.9, 487.1]
      min=-27.2 max=1275.3 mean=511.8045465053556
  [3]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='gaze_y_l'
      sr: type=int shape=None dtype=None
        value=500
      range: type=ndarray shape=(2,) dtype=uint16
        values=[0, 767]
      units: type=str shape=None dtype=None
        value='pixel'
    data: type=ndarray shape=(203008,) dtype=float64
      sample=[582.8, 582.7, 583.0, 583.6, 584.0, 584.3, 584.8, 584.8, 585.3, 585.5, 585.0, 584.4]
      min=-661.1 max=1488.5 mean=418.57300865634073
  [4]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='gaze_x_r'
      sr: type=int shape=None dtype=None
        value=500
      range: type=ndarray shape=(2,) dtype=uint16
        values=[0, 1023]
      units: type=str shape=None dtype=None
        value='pixel'
    data: type=ndarray shape=(203008,) dtype=float64
      sample=[457.0, 456.0, 455.4, 455.3, 455.3, 454.9, 454.2, 453.6, 453.5, 453.4, 453.0, 452.7]
      min=-13.0 max=1251.2 mean=484.43988586737123
  [5]: type=mat_struct shape=None dtype=None
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='gaze_y_r'
      sr: type=int shape=None dtype=None
        value=500
      range: type=ndarray shape=(2,) dtype=uint16
        values=[0, 767]
      units: type=str shape=None dtype=None
        value='pixel'
    data: type=ndarray shape=(203008,) dtype=float64
      sample=[558.2, 557.3, 556.6, 556.5, 557.3, 558.0, 558.2, 558.4, 558.1, 558.0, 557.3, 557.3]
      min=117.3 max=1527.6 mean=415.00305699291727
  [6]: type=mat_struct shape=None dtype=None
    data: type=ndarray shape=(201,) dtype=float64
      sample=[3.0, 5.0, 7.0, 9.0, 11.0, 12.974000000000004, 13.02000000000001, 15.02000000000001, 17.02000000000001, 19.02000000000001, 21.02000000000001, 23.02000000000001]
      min=3.0 max=401.016 mean=201.07674626865676
    markerinfo: type=mat_struct shape=None dtype=None
      name: type=ndarray shape=(201,) dtype=object
        [0]: type=str shape=None dtype=None
          value='M100'
        [1]: type=str shape=None dtype=None
          value='M100'
        [2]: type=str shape=None dtype=None
          value='M100'
        [3]: type=str shape=None dtype=None
          value='M100'
        [4]: type=str shape=None dtype=None
          value='M200'
        [5]: type=str shape=None dtype=None
          value='M400'
        [6]: type=str shape=None dtype=None
          value='M100'
        [7]: type=str shape=None dtype=None
          value='M100'
        [8]: type=str shape=None dtype=None
          value='M100'
        [9]: type=str shape=None dtype=None
          value='M200'
        [10]: type=str shape=None dtype=None
          value='M100'
        [11]: type=str shape=None dtype=None
          value='M100'
      value: type=ndarray shape=(201,) dtype=uint8
        sample=[1, 1, 1, 1, 2, 3, 1, 1, 1, 2, 1, 1]
        min=1.0 max=3.0 mean=1.208955223880597
    header: type=mat_struct shape=None dtype=None
      chantype: type=str shape=None dtype=None
        value='marker'
      units: type=str shape=None dtype=None
        value='events'
      sr: type=int shape=None dtype=None
        value=1

## AOB_UW_cogent_01_sn1.mat

subject: type=mat_struct shape=None dtype=None
  age: type=int shape=None dtype=None
    value=37
  gender: type=str shape=None dtype=None
    value='f'
  screen_dist: type=int shape=None dtype=None
    value=590
  track_dist: type=int shape=None dtype=None
    value=465
  screen_width: type=float shape=None dtype=None
    value=396.68135519705936
  screen_height: type=float shape=None dtype=None
    value=317.34508415764753
data: type=ndarray shape=(40, 5) dtype=uint16
  sample=[1, 6, 0, 0, 0, 2, 10, 76, 466, 1, 3, 16]
  min=0.0 max=755.0 mean=132.305
dataKey: type=ndarray shape=(5,) dtype=object
  [0]: type=mat_struct shape=None dtype=None
    column_type: type=str shape=None dtype=None
      value='trial_index'
    column_index: type=int shape=None dtype=None
      value=1
    column_description: type=str shape=None dtype=None
      value='1. Trial index'
  [1]: type=mat_struct shape=None dtype=None
    column_type: type=str shape=None dtype=None
      value='stimulus_number'
    column_index: type=int shape=None dtype=None
      value=2
    column_description: type=str shape=None dtype=None
      value='2. Number of stimulus (and corresponding marker) from beginning of file'
  [2]: type=mat_struct shape=None dtype=None
    column_type: type=str shape=None dtype=None
      value='key_response_id'
    column_index: type=int shape=None dtype=None
      value=3
    column_description: type=str shape=None dtype=None
      value='3. Pressed key (see Cogent2000 keymap)'
  [3]: type=mat_struct shape=None dtype=None
    column_type: type=str shape=None dtype=None
      value='key_reaction_time'
    column_index: type=int shape=None dtype=None
      value=4
    column_description: type=str shape=None dtype=None
      value='4. Reaction time (ms)'
  [4]: type=mat_struct shape=None dtype=None
    column_type: type=str shape=None dtype=None
      value='key_response_correct'
    column_index: type=int shape=None dtype=None
      value=5
    column_description: type=str shape=None dtype=None
      value='5. Key correct: 0=incorrect [not pressed], 1=correct [pressed]'
