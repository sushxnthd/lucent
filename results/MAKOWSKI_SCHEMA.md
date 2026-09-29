# Makowski drowsiness metadata schema

## README

~~~text
Pipeline to train and evaluate the models

Download data

    download the data in the folder "Data" and store it to a folder: https://osf.io/hmyc4/?view_only=792d6197079f4d239e520a47c900ab96
        specify in config.py where the data is stored

Create config files for all models under investigation

    excecute jupyter notebook create_configs.ipynb to create config files for all models under investigation

Perform HP tuning on first fold to get best parameter setup for CNN, LSTM, Bi-LSTM, and the random forest

    run script run_hp_tuning.sh
        this script creates a json-file "results/best_hp.json" containing the best found params for the first fold.

Rung 5-Fold Cross validation for best found params

    run script run_evaluation.sh
        this scripts creates joblib-files containing the results for the trained models

Plot results

    run the jupyter notebook plot_results.ipynb to create the plots from the paper

Plot shap results for training random forest

    run jupyter notebook shap_rf.ipynb


~~~

## data_format.json

~~~json
{
  "corrupt_vel_right": 0,
  "dx_right": 1,
  "dy_right": 2,
  "x_right": 3,
  "y_right": 4,
  "eye_closure.combined": 5,
  "eye_state.combined": 6,
  "fixations_ivt": 7,
  "saccades_engbert": 8
}
~~~

## label_format.json

~~~json
{
  "block_id": 0,
  "timestamp": 1,
  "same_window_eye_state_500": 2,
  "same_window_eye_state_700": 3,
  "same_window_eye_state_1000": 4,
  "same_window_eye_closure_500": 5,
  "same_window_eye_closure_700": 6,
  "same_window_eye_closure_1000": 7,
  "same_window_eye_corrupt_500": 8,
  "same_window_eye_corrupt_700": 9,
  "same_window_eye_corrupt_1000": 10,
  "upcoming_time_eye_state_500": 11,
  "upcoming_time_eye_state_700": 12,
  "upcoming_time_eye_state_1000": 13,
  "upcoming_time_eye_closure_500": 14,
  "upcoming_time_eye_closure_700": 15,
  "upcoming_time_eye_closure_1000": 16,
  "upcoming_time_eye_corrupt_500": 17,
  "upcoming_time_eye_corrupt_700": 18,
  "upcoming_time_eye_corrupt_1000": 19,
  "interpolated_kss": 20,
  "karolinska_pre": 21,
  "karolinska_post": 22,
  "mean_rt_ms": 23
}
~~~

## array shapes

| array | shape | dtype | unique/sample |
| --- | --- | --- | --- |
| label.npy | (28572, 24) | float64 | [0.0, 1.0, 1.0083231097801533, 1.0166495488042189, 1.0249743232063282, 1.0332974329864817, 1.0416255366325031, 1.0499486464126564, 1.058273420814766, 1.0665981952168753, 1.0749229696189846, 1.083246079399138, 1.0915725184232035, 1.099897292825313, 1.1082237318493784, 1.1165501708734438, 1.1248766098975091, 1.1331997196776626, 1.141524494079772, 1.1498476038599255, 1.1581740428839908, 1.1664988172861002, 1.1748219270662537, 1.183146701468363, 1.1914714758704725, 1.1997945856506258, 1.2081210246746912, 1.2164441344548447, 1.22477057347891, 1.2330936832590635] |
| session_type.npy | (28572,) | <U1 | ['b', 'e', 's'] |
| sub_id.npy | (28572,) | int64 | [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 31, 32] |

## label preview

    [[1.00000000e+00 3.72565500e+06 1.00000000e+00 0.00000000e+00
      0.00000000e+00 1.00000000e+00 0.00000000e+00 0.00000000e+00
      1.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      3.00000000e+00 3.00000000e+00 7.00000000e+00 3.29350000e+02]
     [1.00000000e+00 3.73065500e+06 1.00000000e+00 0.00000000e+00
      0.00000000e+00 1.00000000e+00 0.00000000e+00 0.00000000e+00
      1.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      3.03333306e+00 3.00000000e+00 7.00000000e+00 3.25395000e+02]
     [1.00000000e+00 3.73565600e+06 1.00000000e+00 0.00000000e+00
      0.00000000e+00 1.00000000e+00 0.00000000e+00 0.00000000e+00
      1.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      3.06667278e+00 3.00000000e+00 7.00000000e+00 3.41358333e+02]
     [1.00000000e+00 3.74065600e+06 1.00000000e+00 0.00000000e+00
      0.00000000e+00 1.00000000e+00 0.00000000e+00 0.00000000e+00
      1.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      3.10000583e+00 3.00000000e+00 7.00000000e+00 3.41358333e+02]
     [1.00000000e+00 3.74565700e+06 1.00000000e+00 0.00000000e+00
      0.00000000e+00 1.00000000e+00 0.00000000e+00 0.00000000e+00
      1.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      3.13334556e+00 3.00000000e+00 7.00000000e+00 3.44655000e+02]
     [1.00000000e+00 3.75065900e+06 1.00000000e+00 0.00000000e+00
      0.00000000e+00 1.00000000e+00 0.00000000e+00 0.00000000e+00
      1.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      3.16669194e+00 3.00000000e+00 7.00000000e+00 3.48526000e+02]
     [1.00000000e+00 3.75565900e+06 1.00000000e+00 0.00000000e+00
      0.00000000e+00 1.00000000e+00 0.00000000e+00 0.00000000e+00
      1.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      3.20002500e+00 3.00000000e+00 7.00000000e+00 3.43566667e+02]
     [1.00000000e+00 3.76065900e+06 1.00000000e+00 0.00000000e+00
      0.00000000e+00 1.00000000e+00 0.00000000e+00 0.00000000e+00
      1.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00
      3.23335806e+00 3.00000000e+00 7.00000000e+00 3.43566667e+02]]

## session/sub preview

    session=['e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e'
 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e' 'e'
 'e' 'e' 'e' 'e']
    sub=[3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
 3 3 3]

## human-readable feature names

columns: Unnamed: 0, feature_names, human_readable

    Unnamed: 0,feature_names,human_readable
    0,fixation_texas_median_AccProfMd_R,Median (over fixations) of median accelarations during fixation (deg/s$^2$)~\cite{rigas2018study}
    1,fixation_texas_mean_VelProfSk_R,Mean (over fixations) of skewness values of velocities during fixations (deg/s)~\cite{rigas2018study}
    2,fixation_texas_median_VelProfSk_R,Median (over fixations) of skewness values of velocities during fixations (deg/s)~\cite{rigas2018study}
    3,fixation_texas_median_AccProfMn_R,Median (over fixations) of mean accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    4,fixation_texas_median_VelProfKu_R,Mean (over fixations) of kurtosis values of velocities during fixations (deg/s)~\cite{rigas2018study}
    5,fixation_texas_median_AccProfMd_H,Mean (over fixations) of medians of horizontal accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    6,fixation_texas_mean_VelProfSk_H,Mean (over fixations) of skewness values of horizontal velocities during fixations (deg/s)~\cite{rigas2018study}
    7,fixation_texas_mean_AccProfMd_V,Mean (over fixations) of medians of vertical  accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    8,fixation_texas_median_AccProfMd_V,Median (over fixations) of medians of vertical accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    9,fixation_texas_mean_AccProfMd_R,Mean (over fixations) of medians of accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    10,saccade_texas_mean_direction_h,Mean (over saccades ) of horizontal direction of saccade~\cite{rigas2018study}
    11,fixation_texas_median_AccProfSd_H,Median (over fixations) of standard deviations of horizontal accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    12,fixation_texas_mean_AccProfSd_V,Mean (over fixations) of standard deviations of vertical accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    13,fixation_texas_median_AccProfSd_V,Median (over fixations) of standard deviations of vertical accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    14,fixation_texas_mean_AccProfSd_R,Mean (over fixations) of standard deviations of accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    15,fixation_texas_median_AccProfSd_R,Median (over fixations) of standard deviations of accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    16,fixation_texas_median_DriftAvgSpeed_V,Median (over fixations) of means of vertical drift velocities (deg/s) ~\cite{rigas2018study}
    17,fixation_texas_mean_AccProfSk_H,Mean (over fixations) of skewness values of horizontal accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    18,fixation_texas_median_VelProfSk_H,Median (over fixations) of skewness values of horizontal accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    19,saccade_texas_std_peak_vel_duration_ratio_v,Standard deviation (over saccades) of vertical peak velocities of saccades (deg/s$^2$)~\cite{rigas2018study}
    20,fixation_texas_mean_AccProfMd_H,Mean (over fixations) medians of horizontal accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    21,fixation_texas_median_AccProfSk_H,Mean (over fixations) of  skewness values of horizontal accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    22,fixation_texas_mean_VelProfSk_V,Mean (over fixations) of  skewness values of velocities during fixations (deg/s)~\cite{rigas2018study}
    23,fixation_texas_median_VelProfSk_V,Median (over fixations) of skewness values of velocities during fixations (deg/s)~\cite{rigas2018study}
    24,fixation_texas_median_VelProfMd_R,Median (over fixations) medians of velocities during fixations (deg/s)~\cite{rigas2018study}
    25,fixation_texas_median_VelProfKu_H,Median (over fixations) kurtosis values of horizontal velocities during fixations (deg/s)~\cite{rigas2018study}
    26,fixation_texas_mean_VelProfKu_V,Mean (over fixations) of  kurtosis values of vertical velocities during fixations (deg/s)~\cite{rigas2018study}
    27,fixation_texas_median_VelProfKu_V,Median (over fixations) kurtosis values of vertical velocities during fixations (deg/s)~\cite{rigas2018study}
    28,fixation_texas_median_AccProfKu_H,Median (over fixations) kurtosis values of horizontal accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    29,fixation_texas_mean_VelProfKu_R,Mean (over fixations) of kurtosis values of velocities during fixations (deg/s)~\cite{rigas2018study}
    30,fixation_texas_median_VelProfMd_V,Median (over fixations) medians of vertical velocities during fixations (deg/s)~\cite{rigas2018study}
    31,fixation_texas_mean_AccProfMn_R,Mean (over fixations) of means of accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    32,fixation_texas_median_AccProfMn_H,Median (over fixations) means of horizontal accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    33,fixation_texas_mean_AccProfMn_V,Mean (over fixations) of medians of vertical accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    34,fixation_texas_median_AccProfMn_V,Median (over fixations) means of vertical accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    35,fixation_texas_median_VelProfMd_H,Median (over fixations) medians of horizontal velocities during fixations (deg/s)~\cite{rigas2018study}
    36,fixation_texas_mean_AccProfSk_V,Mean (over fixations) of skewness values of vertical accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    37,fixation_texas_median_AccProfSk_R,Median (over fixations) skewness values of accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    38,fixation_texas_mean_AccProfKu_R,Mean (over fixations) of kurtosis values of accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    39,fixation_texas_median_DriftAvgSpeed_R,Median (over fixations) means of drift velocities (deg/s) ~\cite{rigas2018study}
    40,count_errors,Time steps which are no saccade or fixation
    41,fixation_texas_median_DriftFitQd_R2_H,Median (over fixations) fits for horizontal dirfts during fixations~\cite{rigas2018study}
    42,saccade_texas_median_centroid_v,Median (over saccades) of vertical saccade postions~\cite{rigas2018study}
    43,count_eye_states_2,"Time steps with eye state ""partially open""~Asaphus Vision"
    44,count_eye_states_3,"Time steps with eye state ""downcast""~Asaphus Vision"
    45,eye_closure__mean_standard_closure_speed_max,Mean (over eye closure) of standardized eye closure max speeds~\cite{Schleicher2008}
    46,fixation_texas_median_DriftAvgSpeed_H,Median (over fixations) means of horizontal drift velocities (deg/s)~\cite{rigas2018study}
    47,fixation_texas_std_DriftDist_R,Standard deviation (over fixations) drift distance during fixations~\cite{rigas2018study}
    48,fixation_texas_mean_AccProfSd_H,Mean (over fixations) of standard deviations of horizontal accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    49,saccade_texas_mean_vel_profile_median_r,Mean (over saccades) of medians of velocities during saccades (deg/s)~\cite{rigas2018study}
    50,eye_closure__median_-AVR,Median (over saccades) of ratio of the maximum amplitude to maximum velocity of eyelid movement for the reopening phase~\cite{wilkinson2013the}
    51,saccade_texas_std_peak_vel_duration_ratio_r,Standard deviation (over saccades) peak velocities of saccades (deg/s$^2$)~\cite{rigas2018study}
    52,fixation_texas_skew_VelProfSk_R,Skewness (over fixations) of skewness values of velocities during fixations (deg/s)~\cite{rigas2018study}
    53,saccade_texas_mean_direction,Mean (over saccades) of saccade directions~\cite{rigas2018study}
    54,fixation_texas_mean_DriftDist_H,Mean (over fixations) of horizontal drift distances during fixations~\cite{rigas2018study}
    55,fixation_texas_mean_AccProfSk_R,Mean (over fixations) of skewness values of accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    56,eye_closure__mean_closure_speed_max,mean eye closure maximal speed~\cite{Schleicher2008}
    57,saccade_texas_median_centroid_h,Median (over saccades) of horizontal saccade positions~\cite{rigas2018study}
    58,count_eye_states_0,"Time steps with eye state ""open""~Asaphus Vision"
    59,saccade_texas_std_POC3[MaxIndex],Standard deviation (over saccades) of relative position of greatest deviation between saccadic trajectory and straight line~\cite{doyle2001curved}
    60,fixation_texas_median_PosCentroid_H,Median (over fixations) horizontal fixation positions~\cite{rigas2018study}
    61,fixation_texas_mean_VelProfSd_V,Mean (over fixations) of standard deviations of vertical velocities during fixations (deg/s)~\cite{rigas2018study}
    62,saccade_texas_std_amp_r,Standard deviation for saccadic amplitudes~\cite{rigas2018study}
    63,saccade_texas_std_RawPOC,Standard deviation (over saccades) of deviations between saccadic trajectory and straight line~\cite{doyle2001curved}
    64,eye_closure_TEC,Blink duration (over eye closures) from onset of closing to full reopening~\cite{wilkinson2013the}
    65,saccade_texas_skew_amp_h,Skewness (over saccades) of saccadic amplitudes~\cite{rigas2018study}
    66,eye_closure__mean_BTD,Mean (over eye closures) of blink duration from maximum closing to maximum opening velocity~\cite{wilkinson2013the}
    67,saccade_texas_std_amp_h,Standard deviation (over saccades) saccadic amplitudes~\cite{rigas2018study}
    68,count_fixations,Number of fixations (count)
    69,eye_closure__mean_delay_reopening,Mean (over eye closures) of delay between full closure and onset of reopening\cite{Schleicher2008}
    70,eye_closure__std_delay_reopening,Standard deviation (over eye closures) delay between full closure and onset of reopening\cite{Schleicher2008}
    71,fixation_texas_std_AccProfSk_R,Standard deviation (over saccades) skewness values of accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    72,fixation_texas_mean_AccProfMn_H,Mean (over fixations) of means of horizontal accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    73,fixation_texas_std_AccProfKu_V,Standard deviation (over fixations) kurtosis values of vertical accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    74,saccade_texas_std_vel_profile_mean_v,Standard deviation (over saccades) delay between full closure and onset of reopening~\cite{Schleicher2008}
    75,eye_closure__median_IED,Median (over saccades) of blink durations from maximum closing to maximum opening velocity~\cite{wilkinson2013the}
    76,fixation_texas_skew_AccProfMn_R,Skewness (over fixations) of means of accelerations during fixations (deg/s$^2$)~\cite{rigas2018study}
    77,fixation_texas_std_VelProfSk_V,Standard deviation (over fixations) skewness values of vertical velocities during fixations (deg/s)~\cite{rigas2018study}
    78,eye_closure__std_blink_duration,Standard deviation (over eye closures) blink durations from start to maximum reopening velocity~\cite{Schleicher2008}
    79,eye_closure__mean_IED,Mean (over eye closures) of blink durations from maximum closing to maximum opening velocity~\cite{wilkinson2013the}
    

## participant/session counts

unique subjects: **46**
unique session types: **['b', 'e', 's']**
unique subject/session pairs: **98**