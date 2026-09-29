# Makowski source-code audit for labels and windows

## evaluation.py

### lines 42-63
~~~python
0042:     elif training_mode == 'ordinal_regression':
0043:         suffix = '_' + target + '_' + str(training_mode)
0044:     return suffix
0045: 
0046: 
0047: def get_gt_label(y_all, label_dict,
0048:                  target, training_mode,
0049:                  kss_threshold, kss_normalization,
0050:                  sub_id, session_type_list,
0051:                  label_name = None):
0052:                  
0053:     if training_mode != 'regression':
0054:         kss_normalization = None
0055:     
0056:     # select label to learn on
0057:     if label_name is None:
0058:         if target == 'Sleep':
0059:             label_name = 'upcoming_time_eye_state_1000'
0060:         elif target == 'KSS':
0061:             label_name = 'interpolated_kss'
0062:         elif target == 'reaction_time':
0063:             label_name = 'mean_rt_ms'
~~~

### lines 51-72
~~~python
0051:                  label_name = None):
0052:                  
0053:     if training_mode != 'regression':
0054:         kss_normalization = None
0055:     
0056:     # select label to learn on
0057:     if label_name is None:
0058:         if target == 'Sleep':
0059:             label_name = 'upcoming_time_eye_state_1000'
0060:         elif target == 'KSS':
0061:             label_name = 'interpolated_kss'
0062:         elif target == 'reaction_time':
0063:             label_name = 'mean_rt_ms'
0064: 
0065:     y = y_all[:,label_dict[label_name]]
0066: 
0067:     if target == 'KSS' and training_mode == 'classification':
0068:         y = 1 * (y >= kss_threshold)
0069:     
0070:     elif target == 'KSS' and training_mode == 'regression':
0071:         # For KSS with normalization = 'min-max'
0072:         if kss_normalization == 'min-max':
~~~

### lines 53-74
~~~python
0053:     if training_mode != 'regression':
0054:         kss_normalization = None
0055:     
0056:     # select label to learn on
0057:     if label_name is None:
0058:         if target == 'Sleep':
0059:             label_name = 'upcoming_time_eye_state_1000'
0060:         elif target == 'KSS':
0061:             label_name = 'interpolated_kss'
0062:         elif target == 'reaction_time':
0063:             label_name = 'mean_rt_ms'
0064: 
0065:     y = y_all[:,label_dict[label_name]]
0066: 
0067:     if target == 'KSS' and training_mode == 'classification':
0068:         y = 1 * (y >= kss_threshold)
0069:     
0070:     elif target == 'KSS' and training_mode == 'regression':
0071:         # For KSS with normalization = 'min-max'
0072:         if kss_normalization == 'min-max':
0073:             y_new = y.copy()
0074:             unique_sub_ids = list(np.unique(sub_id))
~~~

### lines 55-76
~~~python
0055:     
0056:     # select label to learn on
0057:     if label_name is None:
0058:         if target == 'Sleep':
0059:             label_name = 'upcoming_time_eye_state_1000'
0060:         elif target == 'KSS':
0061:             label_name = 'interpolated_kss'
0062:         elif target == 'reaction_time':
0063:             label_name = 'mean_rt_ms'
0064: 
0065:     y = y_all[:,label_dict[label_name]]
0066: 
0067:     if target == 'KSS' and training_mode == 'classification':
0068:         y = 1 * (y >= kss_threshold)
0069:     
0070:     elif target == 'KSS' and training_mode == 'regression':
0071:         # For KSS with normalization = 'min-max'
0072:         if kss_normalization == 'min-max':
0073:             y_new = y.copy()
0074:             unique_sub_ids = list(np.unique(sub_id))
0075:             for tmp_sub_id in unique_sub_ids:
0076:                 use_ids = np.where(sub_id == tmp_sub_id)[0]
~~~

### lines 66-87
~~~python
0066: 
0067:     if target == 'KSS' and training_mode == 'classification':
0068:         y = 1 * (y >= kss_threshold)
0069:     
0070:     elif target == 'KSS' and training_mode == 'regression':
0071:         # For KSS with normalization = 'min-max'
0072:         if kss_normalization == 'min-max':
0073:             y_new = y.copy()
0074:             unique_sub_ids = list(np.unique(sub_id))
0075:             for tmp_sub_id in unique_sub_ids:
0076:                 use_ids = np.where(sub_id == tmp_sub_id)[0]
0077:                 cur_vals = y_new[use_ids]
0078:                 min_val = np.min(cur_vals)
0079:                 max_val = np.max(cur_vals)
0080:                 cur_vals = (cur_vals - min_val) / (max_val - min_val)
0081:                 y_new[use_ids] = cur_vals
0082:             y = y_new
0083: 
0084:         # For KSS with normalization = 'baseline'
0085:         elif kss_normalization == 'baseline':
0086:             y_new = y.copy()
0087:             unique_sub_ids = list(np.unique(sub_id))
~~~

### lines 67-88
~~~python
0067:     if target == 'KSS' and training_mode == 'classification':
0068:         y = 1 * (y >= kss_threshold)
0069:     
0070:     elif target == 'KSS' and training_mode == 'regression':
0071:         # For KSS with normalization = 'min-max'
0072:         if kss_normalization == 'min-max':
0073:             y_new = y.copy()
0074:             unique_sub_ids = list(np.unique(sub_id))
0075:             for tmp_sub_id in unique_sub_ids:
0076:                 use_ids = np.where(sub_id == tmp_sub_id)[0]
0077:                 cur_vals = y_new[use_ids]
0078:                 min_val = np.min(cur_vals)
0079:                 max_val = np.max(cur_vals)
0080:                 cur_vals = (cur_vals - min_val) / (max_val - min_val)
0081:                 y_new[use_ids] = cur_vals
0082:             y = y_new
0083: 
0084:         # For KSS with normalization = 'baseline'
0085:         elif kss_normalization == 'baseline':
0086:             y_new = y.copy()
0087:             unique_sub_ids = list(np.unique(sub_id))
0088:             for tmp_sub_id in unique_sub_ids:
~~~

### lines 68-89
~~~python
0068:         y = 1 * (y >= kss_threshold)
0069:     
0070:     elif target == 'KSS' and training_mode == 'regression':
0071:         # For KSS with normalization = 'min-max'
0072:         if kss_normalization == 'min-max':
0073:             y_new = y.copy()
0074:             unique_sub_ids = list(np.unique(sub_id))
0075:             for tmp_sub_id in unique_sub_ids:
0076:                 use_ids = np.where(sub_id == tmp_sub_id)[0]
0077:                 cur_vals = y_new[use_ids]
0078:                 min_val = np.min(cur_vals)
0079:                 max_val = np.max(cur_vals)
0080:                 cur_vals = (cur_vals - min_val) / (max_val - min_val)
0081:                 y_new[use_ids] = cur_vals
0082:             y = y_new
0083: 
0084:         # For KSS with normalization = 'baseline'
0085:         elif kss_normalization == 'baseline':
0086:             y_new = y.copy()
0087:             unique_sub_ids = list(np.unique(sub_id))
0088:             for tmp_sub_id in unique_sub_ids:
0089:                 use_ids = np.where(sub_id == tmp_sub_id)[0]
~~~

### lines 79-100
~~~python
0079:                 max_val = np.max(cur_vals)
0080:                 cur_vals = (cur_vals - min_val) / (max_val - min_val)
0081:                 y_new[use_ids] = cur_vals
0082:             y = y_new
0083: 
0084:         # For KSS with normalization = 'baseline'
0085:         elif kss_normalization == 'baseline':
0086:             y_new = y.copy()
0087:             unique_sub_ids = list(np.unique(sub_id))
0088:             for tmp_sub_id in unique_sub_ids:
0089:                 use_ids = np.where(sub_id == tmp_sub_id)[0]
0090:                 use_ids_baseline = np.where(session_type_list == 'b')[0]
0091:                 baseline_ids = np.array(list(set(use_ids).difference(set(use_ids_baseline))))
0092:                 if len(baseline_ids) == 0:
0093:                     baseline_mean = 5.
0094:                 else:
0095:                     baseline_mean = np.nanmean(y[baseline_ids])
0096:                 # print('    mean: ' + str(baseline_mean))
0097:                 cur_vals = y_new[use_ids]
0098:                 cur_vals = cur_vals / baseline_mean
0099:                 y_new[use_ids] = cur_vals
0100:             y = y_new
~~~

### lines 80-101
~~~python
0080:                 cur_vals = (cur_vals - min_val) / (max_val - min_val)
0081:                 y_new[use_ids] = cur_vals
0082:             y = y_new
0083: 
0084:         # For KSS with normalization = 'baseline'
0085:         elif kss_normalization == 'baseline':
0086:             y_new = y.copy()
0087:             unique_sub_ids = list(np.unique(sub_id))
0088:             for tmp_sub_id in unique_sub_ids:
0089:                 use_ids = np.where(sub_id == tmp_sub_id)[0]
0090:                 use_ids_baseline = np.where(session_type_list == 'b')[0]
0091:                 baseline_ids = np.array(list(set(use_ids).difference(set(use_ids_baseline))))
0092:                 if len(baseline_ids) == 0:
0093:                     baseline_mean = 5.
0094:                 else:
0095:                     baseline_mean = np.nanmean(y[baseline_ids])
0096:                 # print('    mean: ' + str(baseline_mean))
0097:                 cur_vals = y_new[use_ids]
0098:                 cur_vals = cur_vals / baseline_mean
0099:                 y_new[use_ids] = cur_vals
0100:             y = y_new
0101: 
~~~

### lines 81-102
~~~python
0081:                 y_new[use_ids] = cur_vals
0082:             y = y_new
0083: 
0084:         # For KSS with normalization = 'baseline'
0085:         elif kss_normalization == 'baseline':
0086:             y_new = y.copy()
0087:             unique_sub_ids = list(np.unique(sub_id))
0088:             for tmp_sub_id in unique_sub_ids:
0089:                 use_ids = np.where(sub_id == tmp_sub_id)[0]
0090:                 use_ids_baseline = np.where(session_type_list == 'b')[0]
0091:                 baseline_ids = np.array(list(set(use_ids).difference(set(use_ids_baseline))))
0092:                 if len(baseline_ids) == 0:
0093:                     baseline_mean = 5.
0094:                 else:
0095:                     baseline_mean = np.nanmean(y[baseline_ids])
0096:                 # print('    mean: ' + str(baseline_mean))
0097:                 cur_vals = y_new[use_ids]
0098:                 cur_vals = cur_vals / baseline_mean
0099:                 y_new[use_ids] = cur_vals
0100:             y = y_new
0101: 
0102:         # For KSS with normalization = 'no'
~~~

### lines 82-103
~~~python
0082:             y = y_new
0083: 
0084:         # For KSS with normalization = 'baseline'
0085:         elif kss_normalization == 'baseline':
0086:             y_new = y.copy()
0087:             unique_sub_ids = list(np.unique(sub_id))
0088:             for tmp_sub_id in unique_sub_ids:
0089:                 use_ids = np.where(sub_id == tmp_sub_id)[0]
0090:                 use_ids_baseline = np.where(session_type_list == 'b')[0]
0091:                 baseline_ids = np.array(list(set(use_ids).difference(set(use_ids_baseline))))
0092:                 if len(baseline_ids) == 0:
0093:                     baseline_mean = 5.
0094:                 else:
0095:                     baseline_mean = np.nanmean(y[baseline_ids])
0096:                 # print('    mean: ' + str(baseline_mean))
0097:                 cur_vals = y_new[use_ids]
0098:                 cur_vals = cur_vals / baseline_mean
0099:                 y_new[use_ids] = cur_vals
0100:             y = y_new
0101: 
0102:         # For KSS with normalization = 'no'
0103:         elif kss_normalization == 'no':
~~~

### lines 172-193
~~~python
0172:         X_new = np.concatenate([X_new, one_hot_tmp],axis=2)        
0173:     return X_new, out_channel_names
0174: 
0175: def load_nn_data(data_dir,
0176:                  down_sampling = 5,
0177:                  num_parts = 10):
0178:     out_data = []
0179:     for i in range(num_parts):
0180:         cur_data = np.load(data_dir + '/data/' + 'data_down_' + str(down_sampling) + '_' + str(i) + '.npy')
0181:         if i == 0:
0182:             out_data = cur_data
0183:         else:
0184:             out_data = np.concatenate([out_data, cur_data], axis = 0)
0185:     return out_data
0186: 
0187: def devide_data(X_train, y_train, y_all_train, sub_ids,
0188:                 val_frac = 0.15,
0189:                 ):
0190:     num_sub_val = int(np.ceil(len(np.unique(sub_ids)) * val_frac))  # number of subjects in validation data
0191:     sub_val = list(np.random.choice(np.unique(sub_ids), num_sub_val, replace=False))  # ids of subjects
0192:     train_idx = np.isin(sub_ids, sub_val, invert=True)
0193:     validation_idx = np.isin(sub_ids, sub_val, invert=False)
~~~

### lines 179-200
~~~python
0179:     for i in range(num_parts):
0180:         cur_data = np.load(data_dir + '/data/' + 'data_down_' + str(down_sampling) + '_' + str(i) + '.npy')
0181:         if i == 0:
0182:             out_data = cur_data
0183:         else:
0184:             out_data = np.concatenate([out_data, cur_data], axis = 0)
0185:     return out_data
0186: 
0187: def devide_data(X_train, y_train, y_all_train, sub_ids,
0188:                 val_frac = 0.15,
0189:                 ):
0190:     num_sub_val = int(np.ceil(len(np.unique(sub_ids)) * val_frac))  # number of subjects in validation data
0191:     sub_val = list(np.random.choice(np.unique(sub_ids), num_sub_val, replace=False))  # ids of subjects
0192:     train_idx = np.isin(sub_ids, sub_val, invert=True)
0193:     validation_idx = np.isin(sub_ids, sub_val, invert=False)
0194: 
0195:     X_val   = X_train[validation_idx] 
0196:     X_train = X_train[train_idx]
0197:     y_val   = y_train[validation_idx]
0198:     y_train = y_train[train_idx]
0199:     y_all_val = y_all_train[validation_idx]
0200:     y_all_train = y_all_train[train_idx]
~~~

### lines 182-203
~~~python
0182:             out_data = cur_data
0183:         else:
0184:             out_data = np.concatenate([out_data, cur_data], axis = 0)
0185:     return out_data
0186: 
0187: def devide_data(X_train, y_train, y_all_train, sub_ids,
0188:                 val_frac = 0.15,
0189:                 ):
0190:     num_sub_val = int(np.ceil(len(np.unique(sub_ids)) * val_frac))  # number of subjects in validation data
0191:     sub_val = list(np.random.choice(np.unique(sub_ids), num_sub_val, replace=False))  # ids of subjects
0192:     train_idx = np.isin(sub_ids, sub_val, invert=True)
0193:     validation_idx = np.isin(sub_ids, sub_val, invert=False)
0194: 
0195:     X_val   = X_train[validation_idx] 
0196:     X_train = X_train[train_idx]
0197:     y_val   = y_train[validation_idx]
0198:     y_train = y_train[train_idx]
0199:     y_all_val = y_all_train[validation_idx]
0200:     y_all_train = y_all_train[train_idx]
0201:     sub_id_val = sub_ids[validation_idx]
0202:     sub_id_train = sub_ids[train_idx]
0203:     
~~~

### lines 183-204
~~~python
0183:         else:
0184:             out_data = np.concatenate([out_data, cur_data], axis = 0)
0185:     return out_data
0186: 
0187: def devide_data(X_train, y_train, y_all_train, sub_ids,
0188:                 val_frac = 0.15,
0189:                 ):
0190:     num_sub_val = int(np.ceil(len(np.unique(sub_ids)) * val_frac))  # number of subjects in validation data
0191:     sub_val = list(np.random.choice(np.unique(sub_ids), num_sub_val, replace=False))  # ids of subjects
0192:     train_idx = np.isin(sub_ids, sub_val, invert=True)
0193:     validation_idx = np.isin(sub_ids, sub_val, invert=False)
0194: 
0195:     X_val   = X_train[validation_idx] 
0196:     X_train = X_train[train_idx]
0197:     y_val   = y_train[validation_idx]
0198:     y_train = y_train[train_idx]
0199:     y_all_val = y_all_train[validation_idx]
0200:     y_all_train = y_all_train[train_idx]
0201:     sub_id_val = sub_ids[validation_idx]
0202:     sub_id_train = sub_ids[train_idx]
0203:     
0204:     return X_train, X_val, y_train, y_val, y_all_train, y_all_val, sub_id_train, sub_id_val
~~~

### lines 184-205
~~~python
0184:             out_data = np.concatenate([out_data, cur_data], axis = 0)
0185:     return out_data
0186: 
0187: def devide_data(X_train, y_train, y_all_train, sub_ids,
0188:                 val_frac = 0.15,
0189:                 ):
0190:     num_sub_val = int(np.ceil(len(np.unique(sub_ids)) * val_frac))  # number of subjects in validation data
0191:     sub_val = list(np.random.choice(np.unique(sub_ids), num_sub_val, replace=False))  # ids of subjects
0192:     train_idx = np.isin(sub_ids, sub_val, invert=True)
0193:     validation_idx = np.isin(sub_ids, sub_val, invert=False)
0194: 
0195:     X_val   = X_train[validation_idx] 
0196:     X_train = X_train[train_idx]
0197:     y_val   = y_train[validation_idx]
0198:     y_train = y_train[train_idx]
0199:     y_all_val = y_all_train[validation_idx]
0200:     y_all_train = y_all_train[train_idx]
0201:     sub_id_val = sub_ids[validation_idx]
0202:     sub_id_train = sub_ids[train_idx]
0203:     
0204:     return X_train, X_val, y_train, y_val, y_all_train, y_all_val, sub_id_train, sub_id_val
0205: 
~~~

### lines 185-206
~~~python
0185:     return out_data
0186: 
0187: def devide_data(X_train, y_train, y_all_train, sub_ids,
0188:                 val_frac = 0.15,
0189:                 ):
0190:     num_sub_val = int(np.ceil(len(np.unique(sub_ids)) * val_frac))  # number of subjects in validation data
0191:     sub_val = list(np.random.choice(np.unique(sub_ids), num_sub_val, replace=False))  # ids of subjects
0192:     train_idx = np.isin(sub_ids, sub_val, invert=True)
0193:     validation_idx = np.isin(sub_ids, sub_val, invert=False)
0194: 
0195:     X_val   = X_train[validation_idx] 
0196:     X_train = X_train[train_idx]
0197:     y_val   = y_train[validation_idx]
0198:     y_train = y_train[train_idx]
0199:     y_all_val = y_all_train[validation_idx]
0200:     y_all_train = y_all_train[train_idx]
0201:     sub_id_val = sub_ids[validation_idx]
0202:     sub_id_train = sub_ids[train_idx]
0203:     
0204:     return X_train, X_val, y_train, y_val, y_all_train, y_all_val, sub_id_train, sub_id_val
0205: 
0206: def evaluate_config(target = 'Sleep',
~~~

### lines 193-214
~~~python
0193:     validation_idx = np.isin(sub_ids, sub_val, invert=False)
0194: 
0195:     X_val   = X_train[validation_idx] 
0196:     X_train = X_train[train_idx]
0197:     y_val   = y_train[validation_idx]
0198:     y_train = y_train[train_idx]
0199:     y_all_val = y_all_train[validation_idx]
0200:     y_all_train = y_all_train[train_idx]
0201:     sub_id_val = sub_ids[validation_idx]
0202:     sub_id_train = sub_ids[train_idx]
0203:     
0204:     return X_train, X_val, y_train, y_val, y_all_train, y_all_val, sub_id_train, sub_id_val
0205: 
0206: def evaluate_config(target = 'Sleep',
0207:                     kss_normalization = 'no',
0208:                     config_path = None,
0209:                     eval_fold = 0,
0210:                     training_mode = 'classification',
0211:                     kss_threshold = 7,
0212:                     ):
0213:     # params
0214:     random_seed = 42
~~~

### lines 194-215
~~~python
0194: 
0195:     X_val   = X_train[validation_idx] 
0196:     X_train = X_train[train_idx]
0197:     y_val   = y_train[validation_idx]
0198:     y_train = y_train[train_idx]
0199:     y_all_val = y_all_train[validation_idx]
0200:     y_all_train = y_all_train[train_idx]
0201:     sub_id_val = sub_ids[validation_idx]
0202:     sub_id_train = sub_ids[train_idx]
0203:     
0204:     return X_train, X_val, y_train, y_val, y_all_train, y_all_val, sub_id_train, sub_id_val
0205: 
0206: def evaluate_config(target = 'Sleep',
0207:                     kss_normalization = 'no',
0208:                     config_path = None,
0209:                     eval_fold = 0,
0210:                     training_mode = 'classification',
0211:                     kss_threshold = 7,
0212:                     ):
0213:     # params
0214:     random_seed = 42
0215:     num_folds = 5
~~~

### lines 196-217
~~~python
0196:     X_train = X_train[train_idx]
0197:     y_val   = y_train[validation_idx]
0198:     y_train = y_train[train_idx]
0199:     y_all_val = y_all_train[validation_idx]
0200:     y_all_train = y_all_train[train_idx]
0201:     sub_id_val = sub_ids[validation_idx]
0202:     sub_id_train = sub_ids[train_idx]
0203:     
0204:     return X_train, X_val, y_train, y_val, y_all_train, y_all_val, sub_id_train, sub_id_val
0205: 
0206: def evaluate_config(target = 'Sleep',
0207:                     kss_normalization = 'no',
0208:                     config_path = None,
0209:                     eval_fold = 0,
0210:                     training_mode = 'classification',
0211:                     kss_threshold = 7,
0212:                     ):
0213:     # params
0214:     random_seed = 42
0215:     num_folds = 5
0216:     flag_redo = False
0217:     flag_early_stopping = True
~~~

### lines 226-247
~~~python
0226:         config_data['num_classes'] = 2
0227:     elif training_mode == 'regression':
0228:         config_data['num_classes'] = 1
0229:     elif training_mode == 'ordinal_regression':
0230:         config_data['num_classes'] = 9
0231:     config_data['training_mode'] = training_mode
0232:     
0233:     
0234:     label_json_path = data_dir + 'label_format.json'
0235:     label_dict = load_json(label_json_path)
0236:     
0237:     sub_id = np.load(data_dir + 'sub_id.npy')
0238:     session_type_list = np.load(data_dir + 'session_type.npy')
0239:     y_all = np.load(data_dir + 'label.npy')
0240:     
0241:     model_type = config_data['model_type']    
0242:     if model_type == 'rf' or model_type == 'dummy':
0243:         X = np.load(data_dir + 'data/data_rf_big.npy')
0244:     elif model_type == 'cnn_model' or model_type == 'lstm_model' or model_type == 'bi_lstm_model':
0245:         data_json_path = data_dir + 'data_format.json'
0246:         data_format = load_json(data_json_path)
0247:         
~~~

### lines 229-250
~~~python
0229:     elif training_mode == 'ordinal_regression':
0230:         config_data['num_classes'] = 9
0231:     config_data['training_mode'] = training_mode
0232:     
0233:     
0234:     label_json_path = data_dir + 'label_format.json'
0235:     label_dict = load_json(label_json_path)
0236:     
0237:     sub_id = np.load(data_dir + 'sub_id.npy')
0238:     session_type_list = np.load(data_dir + 'session_type.npy')
0239:     y_all = np.load(data_dir + 'label.npy')
0240:     
0241:     model_type = config_data['model_type']    
0242:     if model_type == 'rf' or model_type == 'dummy':
0243:         X = np.load(data_dir + 'data/data_rf_big.npy')
0244:     elif model_type == 'cnn_model' or model_type == 'lstm_model' or model_type == 'bi_lstm_model':
0245:         data_json_path = data_dir + 'data_format.json'
0246:         data_format = load_json(data_json_path)
0247:         
0248:         X = load_nn_data(data_dir = data_dir,
0249:                  down_sampling = config_data['downsampling_factor'],
0250:                  num_parts = 10)
~~~

### lines 230-251
~~~python
0230:         config_data['num_classes'] = 9
0231:     config_data['training_mode'] = training_mode
0232:     
0233:     
0234:     label_json_path = data_dir + 'label_format.json'
0235:     label_dict = load_json(label_json_path)
0236:     
0237:     sub_id = np.load(data_dir + 'sub_id.npy')
0238:     session_type_list = np.load(data_dir + 'session_type.npy')
0239:     y_all = np.load(data_dir + 'label.npy')
0240:     
0241:     model_type = config_data['model_type']    
0242:     if model_type == 'rf' or model_type == 'dummy':
0243:         X = np.load(data_dir + 'data/data_rf_big.npy')
0244:     elif model_type == 'cnn_model' or model_type == 'lstm_model' or model_type == 'bi_lstm_model':
0245:         data_json_path = data_dir + 'data_format.json'
0246:         data_format = load_json(data_json_path)
0247:         
0248:         X = load_nn_data(data_dir = data_dir,
0249:                  down_sampling = config_data['downsampling_factor'],
0250:                  num_parts = 10)
0251:     
~~~

### lines 246-267
~~~python
0246:         data_format = load_json(data_json_path)
0247:         
0248:         X = load_nn_data(data_dir = data_dir,
0249:                  down_sampling = config_data['downsampling_factor'],
0250:                  num_parts = 10)
0251:     
0252:     # get label
0253:     if model_type == 'rf' and training_mode == 'ordinal_regression':
0254:         y = np.int32(np.round(y_all[:, label_dict['interpolated_kss']]))
0255:     else:
0256:         y = get_gt_label(y_all, label_dict,
0257:                  target, training_mode,
0258:                  kss_threshold, kss_normalization,
0259:                  sub_id, session_type_list,
0260:                  )
0261:     
0262:     # set the seed
0263:     np.random.seed(random_seed)
0264:     if len(y.shape) == 2:
0265:         num_classes = y.shape[1]
0266:     else:
0267:         num_classes = 1
~~~

### lines 251-272
~~~python
0251:     
0252:     # get label
0253:     if model_type == 'rf' and training_mode == 'ordinal_regression':
0254:         y = np.int32(np.round(y_all[:, label_dict['interpolated_kss']]))
0255:     else:
0256:         y = get_gt_label(y_all, label_dict,
0257:                  target, training_mode,
0258:                  kss_threshold, kss_normalization,
0259:                  sub_id, session_type_list,
0260:                  )
0261:     
0262:     # set the seed
0263:     np.random.seed(random_seed)
0264:     if len(y.shape) == 2:
0265:         num_classes = y.shape[1]
0266:     else:
0267:         num_classes = 1
0268: 
0269:     if 'rf' not in model_type and 'dummy' not in model_type:
0270:         channel_list = config_data['channel_list']
0271:         scaling_factors = config_data['scaling_factors']
0272:         X, channel_names = transform_data(X, data_format,
~~~

### lines 293-314
~~~python
0293:             model_config['flag_bidirectional'] = False
0294:         elif model_type == 'bi_lstm_model':
0295:             model_config['flag_bidirectional'] = True
0296:     elif 'rf' in model_type:
0297:         flag_early_stopping = False
0298:     
0299:     # create splits
0300:     cv_out = GroupKFold(n_splits=num_folds)
0301:     cv_splits = cv_out.split(np.zeros([len(y),2]), y, sub_id)
0302: 
0303:     fold_counter = 0
0304:     for train, test in tqdm(cv_splits, total=num_folds):
0305:         if fold_counter == eval_fold:
0306:             break
0307:         fold_counter += 1
0308: 
0309:     # training data:
0310:     X_train = X[train]
0311:     y_train = y[train]
0312:     y_all_train = y_all[train]
0313:     sub_id_train = sub_id[train]
0314:     
~~~

### lines 305-326
~~~python
0305:         if fold_counter == eval_fold:
0306:             break
0307:         fold_counter += 1
0308: 
0309:     # training data:
0310:     X_train = X[train]
0311:     y_train = y[train]
0312:     y_all_train = y_all[train]
0313:     sub_id_train = sub_id[train]
0314:     
0315:     # divide train data to validation and train
0316:     if flag_early_stopping:
0317:         X_train, X_val, y_train, y_val, y_all_train, y_all_val, sub_id_train, sub_id_val = devide_data(X_train, y_train, y_all_train, sub_id_train)
0318:     else:
0319:         X_val = None
0320:         y_val = None
0321:         y_all_val = None
0322:         sub_id_val = None    
0323:     
0324:     # test data:
0325:     X_test = X[test]
0326:     y_test = y[test]
~~~

### lines 309-330
~~~python
0309:     # training data:
0310:     X_train = X[train]
0311:     y_train = y[train]
0312:     y_all_train = y_all[train]
0313:     sub_id_train = sub_id[train]
0314:     
0315:     # divide train data to validation and train
0316:     if flag_early_stopping:
0317:         X_train, X_val, y_train, y_val, y_all_train, y_all_val, sub_id_train, sub_id_val = devide_data(X_train, y_train, y_all_train, sub_id_train)
0318:     else:
0319:         X_val = None
0320:         y_val = None
0321:         y_all_val = None
0322:         sub_id_val = None    
0323:     
0324:     # test data:
0325:     X_test = X[test]
0326:     y_test = y[test]
0327:     y_all_test = y_all[test]
0328:     sub_id_test = sub_id[test]
0329:         
0330:     
~~~

### lines 314-335
~~~python
0314:     
0315:     # divide train data to validation and train
0316:     if flag_early_stopping:
0317:         X_train, X_val, y_train, y_val, y_all_train, y_all_val, sub_id_train, sub_id_val = devide_data(X_train, y_train, y_all_train, sub_id_train)
0318:     else:
0319:         X_val = None
0320:         y_val = None
0321:         y_all_val = None
0322:         sub_id_val = None    
0323:     
0324:     # test data:
0325:     X_test = X[test]
0326:     y_test = y[test]
0327:     y_all_test = y_all[test]
0328:     sub_id_test = sub_id[test]
0329:         
0330:     
0331:     # train model
0332:     if 'rf' in model_type:
0333:         param_grid = { 
0334:             'n_estimators': [50, 100, 1000],
0335:             'max_features': ['auto', 'sqrt', 'log2'],
~~~

### lines 320-341
~~~python
0320:         y_val = None
0321:         y_all_val = None
0322:         sub_id_val = None    
0323:     
0324:     # test data:
0325:     X_test = X[test]
0326:     y_test = y[test]
0327:     y_all_test = y_all[test]
0328:     sub_id_test = sub_id[test]
0329:         
0330:     
0331:     # train model
0332:     if 'rf' in model_type:
0333:         param_grid = { 
0334:             'n_estimators': [50, 100, 1000],
0335:             'max_features': ['auto', 'sqrt', 'log2'],
0336:             'max_depth' : [2,4,6,8, None],
0337:             'criterion' :['gini', 'entropy'],
0338:             'n_jobs': [-1]
0339:         }
0340: 
0341:         X_train = np.nan_to_num(X_train, nan=-1)
~~~

### lines 343-364
~~~python
0343: 
0344:         # Step 2: Replace values too large for dtype('float32') into the maximal/minimal possible value
0345:         X_train = np.nan_to_num(X_train.astype(np.float32))
0346:         X_test = np.nan_to_num(X_test.astype(np.float32))
0347: 
0348:         use_ids = np.where(~np.isnan(y_train))[0]
0349:         X_train = X_train[use_ids]
0350:         y_train = y_train[use_ids]
0351:         sub_id_train = sub_id_train[use_ids]
0352: 
0353:         cv_inner = GroupKFold(n_splits=2)
0354:         cv_splits = cv_inner.split(X_train, y_train, sub_id_train)
0355:         if training_mode == 'classification' or training_mode == 'ordinal_regression':
0356:             rf = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_grid, cv=cv_splits)
0357:             rf.fit(X_train, y_train)
0358:             if training_mode == 'classification':
0359:                 prediction = rf.predict_proba(X_test)[:,0]
0360:         elif training_mode == 'regression':
0361:             param_grid.pop('criterion')
0362:             rf = GridSearchCV(estimator=RandomForestRegressor(), param_grid=param_grid, cv=cv_splits)
0363:             rf.fit(X_train, y_train)
0364:             prediction = rf.predict(X_test)
~~~

### lines 346-367
~~~python
0346:         X_test = np.nan_to_num(X_test.astype(np.float32))
0347: 
0348:         use_ids = np.where(~np.isnan(y_train))[0]
0349:         X_train = X_train[use_ids]
0350:         y_train = y_train[use_ids]
0351:         sub_id_train = sub_id_train[use_ids]
0352: 
0353:         cv_inner = GroupKFold(n_splits=2)
0354:         cv_splits = cv_inner.split(X_train, y_train, sub_id_train)
0355:         if training_mode == 'classification' or training_mode == 'ordinal_regression':
0356:             rf = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_grid, cv=cv_splits)
0357:             rf.fit(X_train, y_train)
0358:             if training_mode == 'classification':
0359:                 prediction = rf.predict_proba(X_test)[:,0]
0360:         elif training_mode == 'regression':
0361:             param_grid.pop('criterion')
0362:             rf = GridSearchCV(estimator=RandomForestRegressor(), param_grid=param_grid, cv=cv_splits)
0363:             rf.fit(X_train, y_train)
0364:             prediction = rf.predict(X_test)
0365:         loss = rf.best_score_
0366:     
0367:     elif model_type == 'cnn_model':
~~~

### lines 428-438
~~~python
0428:         prediction = np.ones([X_test.shape[0],]) * np.nanmean(y_train)
0429:         loss = -1
0430:     else:
0431:         print('unknown model_type: ' + str(model_type))
0432:     
0433:     out_dict = {'prediction':prediction,
0434:              'y_test':y_test,
0435:              'y_all_test':y_all_test,
0436:              'sub_id_test':sub_id_test,
0437:              }
0438:     return out_dict, loss
~~~

## run_evaluation.py

## nn_model.py

### lines 19-40
~~~python
0019: from tensorflow.keras.optimizers import Adam
0020: 
0021: import joblib
0022: import numpy as np
0023: from tensorflow.keras.utils import to_categorical
0024: from sklearn.metrics import roc_auc_score
0025: 
0026:         
0027: # create batch by rearanging the sequences
0028: def create_batch_intox(X,y,batch_size=32,
0029:                         class_ratio = .9):
0030:     '''
0031:     X: training data
0032:     y: training label
0033:     batch_size: size of batch
0034:     '''
0035:         
0036:     num_neg = int(batch_size * class_ratio)
0037:     num_pos = batch_size - num_neg
0038:     if len(y.shape) == 2 and y.shape[1] == 2:
0039:         pos_ids = np.where(y[:,0] == 1)[0]
0040:         neg_ids = np.where(y[:,1] == 1)[0]
~~~

### lines 79-100
~~~python
0079:                 name = 'cnn_model'):
0080:         '''
0081:         name: name of model
0082:         '''
0083:         self.name = name
0084:         
0085:     def build_model(self, conv_kernel_sizes,
0086:                 conv_num_filters,
0087:                 conv_strides,
0088:                 dense_layer_sizes,
0089:                 dense_dropout_rates,                
0090:                 num_classes,                
0091:                 seq_len,
0092:                 num_channels,                
0093:                 pooling,
0094:                 use_batch_norm = True,
0095:                 training_mode = 'classification', #classification|ordinal_regression|regression
0096:                 ord_regression_opt = 'mse',
0097:                 flag_use_mha = False,
0098:                 patience = 10,
0099:                 learning_rate = .002,
0100:                 name = 'cnn_model'):
~~~

### lines 96-117
~~~python
0096:                 ord_regression_opt = 'mse',
0097:                 flag_use_mha = False,
0098:                 patience = 10,
0099:                 learning_rate = .002,
0100:                 name = 'cnn_model'):
0101:         '''
0102:         conv_num_filters : list of number of filters
0103:         conv_kernel_sizes: list of kernel-sizes to used
0104:         conv_strides: list of strides for the Conv1D layers
0105:         dense_layer_sizes: list of dense layer sizes
0106:         dense_dropout_rates: dense dropout rates
0107:         flag_use_mha: flag, indicating if we want to use the mulit-head attention
0108:         num_classes: number of classes
0109:         training_mode: training_mode = 'classification', #classification|ordinal_regression|regression
0110:         seq_len: sequence len
0111:         num_channels: number of channels
0112:         use_batch_norm: flag whether to use bach_normalization
0113:         pooling: pooling type used
0114:         patience: patience of early stopping
0115:         learning_rate: learning rate
0116:         ord_regression_opt: optimization criterion for ordinal regresssion (mse | bce)
0117:         name: name for model
~~~

### lines 102-123
~~~python
0102:         conv_num_filters : list of number of filters
0103:         conv_kernel_sizes: list of kernel-sizes to used
0104:         conv_strides: list of strides for the Conv1D layers
0105:         dense_layer_sizes: list of dense layer sizes
0106:         dense_dropout_rates: dense dropout rates
0107:         flag_use_mha: flag, indicating if we want to use the mulit-head attention
0108:         num_classes: number of classes
0109:         training_mode: training_mode = 'classification', #classification|ordinal_regression|regression
0110:         seq_len: sequence len
0111:         num_channels: number of channels
0112:         use_batch_norm: flag whether to use bach_normalization
0113:         pooling: pooling type used
0114:         patience: patience of early stopping
0115:         learning_rate: learning rate
0116:         ord_regression_opt: optimization criterion for ordinal regresssion (mse | bce)
0117:         name: name for model
0118:         '''
0119:         self.config = {'conv_kernel_sizes':conv_kernel_sizes,
0120:                         'conv_num_filters':conv_num_filters,
0121:                         'conv_strides':conv_strides,
0122:                         'dense_layer_sizes':dense_layer_sizes,
0123:                         'dense_dropout_rates':dense_dropout_rates,
~~~

### lines 113-134
~~~python
0113:         pooling: pooling type used
0114:         patience: patience of early stopping
0115:         learning_rate: learning rate
0116:         ord_regression_opt: optimization criterion for ordinal regresssion (mse | bce)
0117:         name: name for model
0118:         '''
0119:         self.config = {'conv_kernel_sizes':conv_kernel_sizes,
0120:                         'conv_num_filters':conv_num_filters,
0121:                         'conv_strides':conv_strides,
0122:                         'dense_layer_sizes':dense_layer_sizes,
0123:                         'dense_dropout_rates':dense_dropout_rates,
0124:                         'flag_use_mha':flag_use_mha,
0125:                         'num_classes':num_classes,
0126:                         'training_mode':training_mode,
0127:                         'seq_len':seq_len,
0128:                         'num_channels': num_channels,
0129:                         'use_batch_norm': use_batch_norm,
0130:                         'pooling': pooling,
0131:                         'patience':patience,
0132:                         'learning_rate':learning_rate,                        
0133:                         'name':name}
0134:         
~~~

### lines 136-157
~~~python
0136:         tf.keras.backend.clear_session()
0137:         input_raw = Input(shape=(seq_len, num_channels), name='input_raw')
0138:         
0139:         
0140:         prev_layer = input_raw
0141:         for j in range(len(conv_kernel_sizes)):
0142:             conv_layer = Conv1D(   filters=conv_num_filters[j],
0143:                                                 kernel_size=conv_kernel_sizes[j],
0144:                                                 strides=conv_strides[j],
0145:                                                 padding='same',
0146:                                                 kernel_initializer='he_normal',
0147:                                                 name='conv_1d_' + str(j+1)
0148:                                             )(prev_layer)
0149:             if use_batch_norm:
0150:                 conv_layer = BatchNormalization()(conv_layer)
0151:             conv_layer = ReLU()(conv_layer)
0152:             prev_layer = conv_layer
0153:         
0154:         if pooling == "average":
0155:             pool_layer = GlobalAveragePooling1D()(prev_layer)
0156:         elif pooling == "max":
0157:             pool_layer = GlobalMaxPool1D()(prev_layer)
~~~

### lines 215-236
~~~python
0215:         config_path = model_path + '.joblib'
0216:         weights_path = model_path + '.h5'
0217:         self.config = joblib.load(config_path)
0218:         self.build_model_from_config(self.config)
0219:         if load_weights:
0220:             self.model.load_weights(weights_path)
0221:     
0222:     
0223:     def hyperparameter_tuning(self, X_train, y_train, sub_id_train,
0224:                             param_grid = None,
0225:                             seq_len = 10000,
0226:                             num_channels = 7,
0227:                             val_frac=0.15,
0228:                             batch_size = 16, epochs = 100,
0229:                             perform_grid_search = True,
0230:                             ):
0231:         if perform_grid_search:
0232:             val_losses = []
0233:             use_grids = []
0234:             for i in range(len(param_grid)):
0235:                 cur_grid = param_grid[i]
0236:                 cur_grid['seq_len'] = seq_len
~~~

### lines 234-255
~~~python
0234:             for i in range(len(param_grid)):
0235:                 cur_grid = param_grid[i]
0236:                 cur_grid['seq_len'] = seq_len
0237:                 cur_grid['num_channels'] = num_channels
0238: 
0239:                 self.build_model_from_config(cur_grid)
0240:                 use_grids.append(cur_grid)
0241: 
0242:                 num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0243:                 sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0244:                 train_idx = np.isin(sub_id_train, sub_val, invert=True)
0245:                 validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0246: 
0247:                 X_cross_train = X_train[train_idx]
0248:                 X_cross_val = X_train[validation_idx]        
0249: 
0250:                 y_cross_train = y_train[train_idx]
0251:                 y_cross_val = y_train[validation_idx]
0252: 
0253:                 history = self.fit(X_cross_train, y_cross_train,
0254:                         X_cross_val, y_cross_val,
0255:                           batch_size = batch_size,
~~~

### lines 235-256
~~~python
0235:                 cur_grid = param_grid[i]
0236:                 cur_grid['seq_len'] = seq_len
0237:                 cur_grid['num_channels'] = num_channels
0238: 
0239:                 self.build_model_from_config(cur_grid)
0240:                 use_grids.append(cur_grid)
0241: 
0242:                 num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0243:                 sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0244:                 train_idx = np.isin(sub_id_train, sub_val, invert=True)
0245:                 validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0246: 
0247:                 X_cross_train = X_train[train_idx]
0248:                 X_cross_val = X_train[validation_idx]        
0249: 
0250:                 y_cross_train = y_train[train_idx]
0251:                 y_cross_val = y_train[validation_idx]
0252: 
0253:                 history = self.fit(X_cross_train, y_cross_train,
0254:                         X_cross_val, y_cross_val,
0255:                           batch_size = batch_size,
0256:                           )
~~~

### lines 236-257
~~~python
0236:                 cur_grid['seq_len'] = seq_len
0237:                 cur_grid['num_channels'] = num_channels
0238: 
0239:                 self.build_model_from_config(cur_grid)
0240:                 use_grids.append(cur_grid)
0241: 
0242:                 num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0243:                 sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0244:                 train_idx = np.isin(sub_id_train, sub_val, invert=True)
0245:                 validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0246: 
0247:                 X_cross_train = X_train[train_idx]
0248:                 X_cross_val = X_train[validation_idx]        
0249: 
0250:                 y_cross_train = y_train[train_idx]
0251:                 y_cross_val = y_train[validation_idx]
0252: 
0253:                 history = self.fit(X_cross_train, y_cross_train,
0254:                         X_cross_val, y_cross_val,
0255:                           batch_size = batch_size,
0256:                           )
0257: 
~~~

### lines 237-258
~~~python
0237:                 cur_grid['num_channels'] = num_channels
0238: 
0239:                 self.build_model_from_config(cur_grid)
0240:                 use_grids.append(cur_grid)
0241: 
0242:                 num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0243:                 sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0244:                 train_idx = np.isin(sub_id_train, sub_val, invert=True)
0245:                 validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0246: 
0247:                 X_cross_train = X_train[train_idx]
0248:                 X_cross_val = X_train[validation_idx]        
0249: 
0250:                 y_cross_train = y_train[train_idx]
0251:                 y_cross_val = y_train[validation_idx]
0252: 
0253:                 history = self.fit(X_cross_train, y_cross_train,
0254:                         X_cross_val, y_cross_val,
0255:                           batch_size = batch_size,
0256:                           )
0257: 
0258:                 val_loss = history.history['val_loss'][-1]
~~~

### lines 328-349
~~~python
0328:                                                  class_ratio = class_ratio),
0329:                                  steps_per_epoch=len(X_train) // batch_size,
0330:                                  epochs=epochs)
0331:                      
0332:         return history
0333:     
0334:     
0335:     def evaluate_with_hyper_tuning(self,
0336:                                     X_train, X_test, y_train, y_test, sub_id_train, val_frac=0.15,
0337:                                     param_grid = None,
0338:                                     seq_len = 10000,
0339:                                     num_channels = 7,
0340:                                     batch_size = 16, epochs = 100,
0341:                                     perform_grid_search = True,
0342:                                     ):
0343:                                   
0344:         # HP tuning
0345:         best_params = self.hyperparameter_tuning(X_train, y_train, sub_id_train,
0346:                             param_grid = param_grid,
0347:                             seq_len = seq_len,
0348:                             num_channels = num_channels,
0349:                             val_frac=val_frac,
~~~

### lines 337-358
~~~python
0337:                                     param_grid = None,
0338:                                     seq_len = 10000,
0339:                                     num_channels = 7,
0340:                                     batch_size = 16, epochs = 100,
0341:                                     perform_grid_search = True,
0342:                                     ):
0343:                                   
0344:         # HP tuning
0345:         best_params = self.hyperparameter_tuning(X_train, y_train, sub_id_train,
0346:                             param_grid = param_grid,
0347:                             seq_len = seq_len,
0348:                             num_channels = num_channels,
0349:                             val_frac=val_frac,
0350:                             perform_grid_search = perform_grid_search,
0351:                             )
0352:         
0353:         # model training
0354:         self.build_model_from_config(best_params)
0355:         num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0356:         sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0357:         train_idx = np.isin(sub_id_train, sub_val, invert=True)
0358:         validation_idx = np.isin(sub_id_train, sub_val, invert=False)
~~~

### lines 347-368
~~~python
0347:                             seq_len = seq_len,
0348:                             num_channels = num_channels,
0349:                             val_frac=val_frac,
0350:                             perform_grid_search = perform_grid_search,
0351:                             )
0352:         
0353:         # model training
0354:         self.build_model_from_config(best_params)
0355:         num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0356:         sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0357:         train_idx = np.isin(sub_id_train, sub_val, invert=True)
0358:         validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0359:                     
0360:         X_cross_train = X_train[train_idx]
0361:         X_cross_val = X_train[validation_idx]        
0362:         
0363:         y_cross_train = y_train[train_idx]
0364:         y_cross_val = y_train[validation_idx]
0365:         
0366:         history = self.fit(X_cross_train, y_cross_train,
0367:                 X_cross_val, y_cross_val,
0368:                 batch_size = batch_size, epochs = 100,
~~~

### lines 348-369
~~~python
0348:                             num_channels = num_channels,
0349:                             val_frac=val_frac,
0350:                             perform_grid_search = perform_grid_search,
0351:                             )
0352:         
0353:         # model training
0354:         self.build_model_from_config(best_params)
0355:         num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0356:         sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0357:         train_idx = np.isin(sub_id_train, sub_val, invert=True)
0358:         validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0359:                     
0360:         X_cross_train = X_train[train_idx]
0361:         X_cross_val = X_train[validation_idx]        
0362:         
0363:         y_cross_train = y_train[train_idx]
0364:         y_cross_val = y_train[validation_idx]
0365:         
0366:         history = self.fit(X_cross_train, y_cross_train,
0367:                 X_cross_val, y_cross_val,
0368:                 batch_size = batch_size, epochs = 100,
0369:                 )
~~~

### lines 349-370
~~~python
0349:                             val_frac=val_frac,
0350:                             perform_grid_search = perform_grid_search,
0351:                             )
0352:         
0353:         # model training
0354:         self.build_model_from_config(best_params)
0355:         num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0356:         sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0357:         train_idx = np.isin(sub_id_train, sub_val, invert=True)
0358:         validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0359:                     
0360:         X_cross_train = X_train[train_idx]
0361:         X_cross_val = X_train[validation_idx]        
0362:         
0363:         y_cross_train = y_train[train_idx]
0364:         y_cross_val = y_train[validation_idx]
0365:         
0366:         history = self.fit(X_cross_train, y_cross_train,
0367:                 X_cross_val, y_cross_val,
0368:                 batch_size = batch_size, epochs = 100,
0369:                 )
0370:         
~~~

### lines 350-371
~~~python
0350:                             perform_grid_search = perform_grid_search,
0351:                             )
0352:         
0353:         # model training
0354:         self.build_model_from_config(best_params)
0355:         num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0356:         sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0357:         train_idx = np.isin(sub_id_train, sub_val, invert=True)
0358:         validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0359:                     
0360:         X_cross_train = X_train[train_idx]
0361:         X_cross_val = X_train[validation_idx]        
0362:         
0363:         y_cross_train = y_train[train_idx]
0364:         y_cross_val = y_train[validation_idx]
0365:         
0366:         history = self.fit(X_cross_train, y_cross_train,
0367:                 X_cross_val, y_cross_val,
0368:                 batch_size = batch_size, epochs = 100,
0369:                 )
0370:         
0371:         # test model        
~~~

### lines 395-416
~~~python
0395:                 ord_regression_opt = 'mse',
0396:                 patience = 10,
0397:                 learning_rate = .002,
0398:                 name = 'rnn_model'):
0399:         '''
0400:         lstm_units : list of number hidden units for LSTM layers
0401:         flag_bidirectional: whether we want to use bidirectional
0402:         conv_kernel_sizes: list of kernel-sizes to used
0403:         conv_strides: list of strides for the Conv1D layers
0404:         dense_layer_sizes: list of dense layer sizes
0405:         dense_dropout_rates: dense dropout rates
0406:         flag_use_mha: flag, indicating if we want to use the mulit-head attention
0407:         num_classes: number of classes
0408:         training_mode : classification|ordinal_regression|regression
0409:         seq_len: sequence len
0410:         num_channels: number of channels
0411:         use_batch_norm: flag whether to use bach_normalization
0412:         pooling: pooling type used
0413:         patience: patience of early stopping
0414:         ord_regression_opt: optimization criterion for ordinal regresssion (mse | bce)
0415:         learning_rate: learning rate
0416:         name: name for model
~~~

### lines 401-422
~~~python
0401:         flag_bidirectional: whether we want to use bidirectional
0402:         conv_kernel_sizes: list of kernel-sizes to used
0403:         conv_strides: list of strides for the Conv1D layers
0404:         dense_layer_sizes: list of dense layer sizes
0405:         dense_dropout_rates: dense dropout rates
0406:         flag_use_mha: flag, indicating if we want to use the mulit-head attention
0407:         num_classes: number of classes
0408:         training_mode : classification|ordinal_regression|regression
0409:         seq_len: sequence len
0410:         num_channels: number of channels
0411:         use_batch_norm: flag whether to use bach_normalization
0412:         pooling: pooling type used
0413:         patience: patience of early stopping
0414:         ord_regression_opt: optimization criterion for ordinal regresssion (mse | bce)
0415:         learning_rate: learning rate
0416:         name: name for model
0417:         '''
0418:         self.config = {'lstm_units':lstm_units,
0419:                         'flag_bidirectional':flag_bidirectional,
0420:                         'dense_layer_sizes':dense_layer_sizes,
0421:                         'dense_dropout_rates':dense_dropout_rates,
0422:                         'num_classes':num_classes,
~~~

### lines 430-451
~~~python
0430:                         'name':name}
0431:         
0432:         self.name = name
0433:         tf.keras.backend.clear_session()
0434:         input_raw = Input(shape=(seq_len, num_channels), name='input_raw')
0435:         
0436:         
0437:         prev_layer = input_raw
0438:         return_sequences = True
0439:         for j in range(len(lstm_units)):
0440:             if j == len(lstm_units) - 1:
0441:                 return_sequences = False
0442:             if flag_bidirectional:
0443:                 lstm = Bidirectional(
0444:                     LSTM(units=lstm_units[j], return_sequences=return_sequences), name='bi-lstm_' + str(j+1))(prev_layer)
0445:                 prev_layer = lstm
0446:             else:
0447:                 lstm = LSTM(units=lstm_units[j], return_sequences=return_sequences, name='lstm_' + str(j+1))(prev_layer)
0448:                 prev_layer = lstm
0449:                 
0450:         # flatten
0451:         flatten = Flatten(name='flatten')(prev_layer)
~~~

### lines 433-454
~~~python
0433:         tf.keras.backend.clear_session()
0434:         input_raw = Input(shape=(seq_len, num_channels), name='input_raw')
0435:         
0436:         
0437:         prev_layer = input_raw
0438:         return_sequences = True
0439:         for j in range(len(lstm_units)):
0440:             if j == len(lstm_units) - 1:
0441:                 return_sequences = False
0442:             if flag_bidirectional:
0443:                 lstm = Bidirectional(
0444:                     LSTM(units=lstm_units[j], return_sequences=return_sequences), name='bi-lstm_' + str(j+1))(prev_layer)
0445:                 prev_layer = lstm
0446:             else:
0447:                 lstm = LSTM(units=lstm_units[j], return_sequences=return_sequences, name='lstm_' + str(j+1))(prev_layer)
0448:                 prev_layer = lstm
0449:                 
0450:         # flatten
0451:         flatten = Flatten(name='flatten')(prev_layer)
0452:         
0453:         # add dense layers        
0454:         prev_layer = flatten
~~~

### lines 436-457
~~~python
0436:         
0437:         prev_layer = input_raw
0438:         return_sequences = True
0439:         for j in range(len(lstm_units)):
0440:             if j == len(lstm_units) - 1:
0441:                 return_sequences = False
0442:             if flag_bidirectional:
0443:                 lstm = Bidirectional(
0444:                     LSTM(units=lstm_units[j], return_sequences=return_sequences), name='bi-lstm_' + str(j+1))(prev_layer)
0445:                 prev_layer = lstm
0446:             else:
0447:                 lstm = LSTM(units=lstm_units[j], return_sequences=return_sequences, name='lstm_' + str(j+1))(prev_layer)
0448:                 prev_layer = lstm
0449:                 
0450:         # flatten
0451:         flatten = Flatten(name='flatten')(prev_layer)
0452:         
0453:         # add dense layers        
0454:         prev_layer = flatten
0455:         for j in range(len(dense_layer_sizes)):
0456:             dense_layer = Dense(dense_layer_sizes[j], activation='relu', name = 'dense_' + str(j+1))(prev_layer)
0457:             dropout_layer = Dropout(dense_dropout_rates[j])(dense_layer)
~~~

### lines 439-460
~~~python
0439:         for j in range(len(lstm_units)):
0440:             if j == len(lstm_units) - 1:
0441:                 return_sequences = False
0442:             if flag_bidirectional:
0443:                 lstm = Bidirectional(
0444:                     LSTM(units=lstm_units[j], return_sequences=return_sequences), name='bi-lstm_' + str(j+1))(prev_layer)
0445:                 prev_layer = lstm
0446:             else:
0447:                 lstm = LSTM(units=lstm_units[j], return_sequences=return_sequences, name='lstm_' + str(j+1))(prev_layer)
0448:                 prev_layer = lstm
0449:                 
0450:         # flatten
0451:         flatten = Flatten(name='flatten')(prev_layer)
0452:         
0453:         # add dense layers        
0454:         prev_layer = flatten
0455:         for j in range(len(dense_layer_sizes)):
0456:             dense_layer = Dense(dense_layer_sizes[j], activation='relu', name = 'dense_' + str(j+1))(prev_layer)
0457:             dropout_layer = Dropout(dense_dropout_rates[j])(dense_layer)
0458:             prev_layer = dropout_layer
0459:         
0460:         
~~~

### lines 497-518
~~~python
0497:         config_path = model_path + '.joblib'
0498:         weights_path = model_path + '.h5'
0499:         self.config = joblib.load(config_path)
0500:         self.build_model_from_config(self.config)
0501:         if load_weights:
0502:             self.model.load_weights(weights_path)
0503:     
0504:     
0505:     def hyperparameter_tuning(self, X_train, y_train, sub_id_train,
0506:                             param_grid = None,
0507:                             seq_len = 10000,
0508:                             num_channels = 7,
0509:                             val_frac=0.15,
0510:                             batch_size = 16, epochs = 100,
0511:                             flag_bidirectional = False,
0512:                             perform_grid_search = False,
0513:                             ):
0514:         
0515:         if perform_grid_search:
0516:             val_losses = []
0517:             use_grids = []
0518:             for i in range(len(param_grid)):
~~~

### lines 518-539
~~~python
0518:             for i in range(len(param_grid)):
0519:                 cur_grid = param_grid[i]
0520:                 cur_grid['seq_len'] = seq_len
0521:                 cur_grid['num_channels'] = num_channels
0522: 
0523:                 self.build_model_from_config(cur_grid)
0524:                 use_grids.append(cur_grid)
0525: 
0526:                 num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0527:                 sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0528:                 train_idx = np.isin(sub_id_train, sub_val, invert=True)
0529:                 validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0530: 
0531:                 X_cross_train = X_train[train_idx]
0532:                 X_cross_val = X_train[validation_idx]        
0533: 
0534:                 y_cross_train = y_train[train_idx]
0535:                 y_cross_val = y_train[validation_idx]
0536: 
0537:                 history = self.fit(X_cross_train, y_cross_train,
0538:                         X_cross_val, y_cross_val,
0539:                           batch_size = batch_size,
~~~

### lines 519-540
~~~python
0519:                 cur_grid = param_grid[i]
0520:                 cur_grid['seq_len'] = seq_len
0521:                 cur_grid['num_channels'] = num_channels
0522: 
0523:                 self.build_model_from_config(cur_grid)
0524:                 use_grids.append(cur_grid)
0525: 
0526:                 num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0527:                 sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0528:                 train_idx = np.isin(sub_id_train, sub_val, invert=True)
0529:                 validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0530: 
0531:                 X_cross_train = X_train[train_idx]
0532:                 X_cross_val = X_train[validation_idx]        
0533: 
0534:                 y_cross_train = y_train[train_idx]
0535:                 y_cross_val = y_train[validation_idx]
0536: 
0537:                 history = self.fit(X_cross_train, y_cross_train,
0538:                         X_cross_val, y_cross_val,
0539:                           batch_size = batch_size,
0540:                           )
~~~

### lines 520-541
~~~python
0520:                 cur_grid['seq_len'] = seq_len
0521:                 cur_grid['num_channels'] = num_channels
0522: 
0523:                 self.build_model_from_config(cur_grid)
0524:                 use_grids.append(cur_grid)
0525: 
0526:                 num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0527:                 sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0528:                 train_idx = np.isin(sub_id_train, sub_val, invert=True)
0529:                 validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0530: 
0531:                 X_cross_train = X_train[train_idx]
0532:                 X_cross_val = X_train[validation_idx]        
0533: 
0534:                 y_cross_train = y_train[train_idx]
0535:                 y_cross_val = y_train[validation_idx]
0536: 
0537:                 history = self.fit(X_cross_train, y_cross_train,
0538:                         X_cross_val, y_cross_val,
0539:                           batch_size = batch_size,
0540:                           )
0541: 
~~~

### lines 521-542
~~~python
0521:                 cur_grid['num_channels'] = num_channels
0522: 
0523:                 self.build_model_from_config(cur_grid)
0524:                 use_grids.append(cur_grid)
0525: 
0526:                 num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0527:                 sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0528:                 train_idx = np.isin(sub_id_train, sub_val, invert=True)
0529:                 validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0530: 
0531:                 X_cross_train = X_train[train_idx]
0532:                 X_cross_val = X_train[validation_idx]        
0533: 
0534:                 y_cross_train = y_train[train_idx]
0535:                 y_cross_val = y_train[validation_idx]
0536: 
0537:                 history = self.fit(X_cross_train, y_cross_train,
0538:                         X_cross_val, y_cross_val,
0539:                           batch_size = batch_size,
0540:                           )
0541: 
0542:                 val_loss = history.history['val_loss'][-1]
~~~

### lines 613-634
~~~python
0613:                                  steps_per_epoch=len(X_train) // batch_size,
0614:                                  epochs=epochs)
0615:                      
0616:         return history
0617:     
0618:     
0619:     
0620:     def evaluate_with_hyper_tuning(self,
0621:                                     X_train, X_test, y_train, y_test, sub_id_train, val_frac=0.15,
0622:                                     param_grid = None,
0623:                                     seq_len = 10000,
0624:                                     num_channels = 7,
0625:                                     batch_size = 16, epochs = 100,
0626:                                     flag_bidirectional = False,
0627:                                     perform_grid_search = False,
0628:                                     ):
0629:                                   
0630:         # HP tuning
0631:         best_params = self.hyperparameter_tuning(X_train, y_train, sub_id_train,
0632:                             param_grid = param_grid,
0633:                             seq_len = seq_len,
0634:                             num_channels = num_channels,
~~~

### lines 623-644
~~~python
0623:                                     seq_len = 10000,
0624:                                     num_channels = 7,
0625:                                     batch_size = 16, epochs = 100,
0626:                                     flag_bidirectional = False,
0627:                                     perform_grid_search = False,
0628:                                     ):
0629:                                   
0630:         # HP tuning
0631:         best_params = self.hyperparameter_tuning(X_train, y_train, sub_id_train,
0632:                             param_grid = param_grid,
0633:                             seq_len = seq_len,
0634:                             num_channels = num_channels,
0635:                             val_frac=val_frac,
0636:                             flag_bidirectional = flag_bidirectional,
0637:                             perform_grid_search = perform_grid_search,
0638:                             )
0639:         
0640:         # model training
0641:         self.build_model_from_config(best_params)
0642:         num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0643:         sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0644:         train_idx = np.isin(sub_id_train, sub_val, invert=True)
~~~

### lines 634-655
~~~python
0634:                             num_channels = num_channels,
0635:                             val_frac=val_frac,
0636:                             flag_bidirectional = flag_bidirectional,
0637:                             perform_grid_search = perform_grid_search,
0638:                             )
0639:         
0640:         # model training
0641:         self.build_model_from_config(best_params)
0642:         num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0643:         sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0644:         train_idx = np.isin(sub_id_train, sub_val, invert=True)
0645:         validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0646:                     
0647:         X_cross_train = X_train[train_idx]
0648:         X_cross_val = X_train[validation_idx]        
0649:         
0650:         y_cross_train = y_train[train_idx]
0651:         y_cross_val = y_train[validation_idx]
0652:         
0653:         history = self.fit(X_cross_train, y_cross_train,
0654:                 X_cross_val, y_cross_val,
0655:                 batch_size = batch_size, epochs = 100,
~~~

### lines 635-656
~~~python
0635:                             val_frac=val_frac,
0636:                             flag_bidirectional = flag_bidirectional,
0637:                             perform_grid_search = perform_grid_search,
0638:                             )
0639:         
0640:         # model training
0641:         self.build_model_from_config(best_params)
0642:         num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0643:         sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0644:         train_idx = np.isin(sub_id_train, sub_val, invert=True)
0645:         validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0646:                     
0647:         X_cross_train = X_train[train_idx]
0648:         X_cross_val = X_train[validation_idx]        
0649:         
0650:         y_cross_train = y_train[train_idx]
0651:         y_cross_val = y_train[validation_idx]
0652:         
0653:         history = self.fit(X_cross_train, y_cross_train,
0654:                 X_cross_val, y_cross_val,
0655:                 batch_size = batch_size, epochs = 100,
0656:                 )
~~~

### lines 636-657
~~~python
0636:                             flag_bidirectional = flag_bidirectional,
0637:                             perform_grid_search = perform_grid_search,
0638:                             )
0639:         
0640:         # model training
0641:         self.build_model_from_config(best_params)
0642:         num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0643:         sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0644:         train_idx = np.isin(sub_id_train, sub_val, invert=True)
0645:         validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0646:                     
0647:         X_cross_train = X_train[train_idx]
0648:         X_cross_val = X_train[validation_idx]        
0649:         
0650:         y_cross_train = y_train[train_idx]
0651:         y_cross_val = y_train[validation_idx]
0652:         
0653:         history = self.fit(X_cross_train, y_cross_train,
0654:                 X_cross_val, y_cross_val,
0655:                 batch_size = batch_size, epochs = 100,
0656:                 )
0657:         
~~~

### lines 637-658
~~~python
0637:                             perform_grid_search = perform_grid_search,
0638:                             )
0639:         
0640:         # model training
0641:         self.build_model_from_config(best_params)
0642:         num_sub_val = int(np.ceil(len(np.unique(sub_id_train)) * val_frac))  # number of subjects in validation data
0643:         sub_val = list(np.random.choice(np.unique(sub_id_train), num_sub_val, replace=False))  # ids of subjects
0644:         train_idx = np.isin(sub_id_train, sub_val, invert=True)
0645:         validation_idx = np.isin(sub_id_train, sub_val, invert=False)
0646:                     
0647:         X_cross_train = X_train[train_idx]
0648:         X_cross_val = X_train[validation_idx]        
0649:         
0650:         y_cross_train = y_train[train_idx]
0651:         y_cross_val = y_train[validation_idx]
0652:         
0653:         history = self.fit(X_cross_train, y_cross_train,
0654:                 X_cross_val, y_cross_val,
0655:                 batch_size = batch_size, epochs = 100,
0656:                 )
0657:         
0658:         # test model        
~~~
