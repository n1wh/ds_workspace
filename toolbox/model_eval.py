import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import roc_curve, precision_recall_curve, auc
from sklearn.metrics import confusion_matrix, roc_auc_score, f1_score

from sklearn.calibration import calibration_curve

from sklearn.metrics import roc_auc_score


def eval_classifier(y_true: np.array, y_pred_prob: np.array, target_class_thr: float=0.5, model=None, return_thr_tables: bool=False) -> None:
    
    y_pred = [1 if row[1] >= thr else 0 for row in y_pred_prob]
    y_target_prob = y_pred_prob[:, 1]
    
    # print out a general classification report
    print(
        f"Classification report:\n\tModel: {model}\n\n"
        f"{metrics.classification_report(y_true, y_pred)}"
    )
    
    # calculate Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    TP = cm[1, 1]
    TN = cm[0, 0]
    FP = cm[0, 1]
    FN = cm[1, 0]

    # accuracy from confusion matrix
    acc = (TP + TN) / (TP + TN + FP + FN)
    float_precision = 4
    print ('Accuracy:', round(acc, float_precision))

    # recall for negative class
    specificity = TN / (TN + FP)
    print('Specificity:', round(specificity, float_precision))
    
    # recall for positive calss
    sensitivity = TP / (FN + TP)
    print('Sensitivity:', round(sensitivity, float_precision))

    # init figure for charts
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(18,5))
    font_size = 14
    
    # draw Confusion Matrix as heatmap
    sns.heatmap(cm, annot=True, cmap='YlOrRd', fmt='1', linewidth=0.1, linecolor='grey', ax=ax[0])
    cm_ax = ax[0]
    cm_ax.set_title('Confusion Matrix')
    cm_ax.set_xlabel('Predicted', fontsize=font_size)
    cm_ax.set_ylabel('True', fontsize=font_size)
    
    # calculate roc curves
    fpr, tpr, thresholds = roc_curve(y_test, y_target_prob)#, pos_label=9)
    roc_auc = round(roc_auc_score(y_true, y_target_prob), float_precision)
    
    if return_thr_tables == True:
        threshold_table = list(zip(thresholds, tpr, fpr))
        roc_curve_df = pd.DataFrame(threshold_table, columns=['threshold', 'sensitivity', 'specificity']).sort_values(by='threshold', ascending=False)

    # draw ROC Curve (Error Curve)
    roc_ax = ax[1]
    roc_ax.plot(fpr, tpr, marker=None, label='Model', color='red')
    roc_ax.plot([0, 1], linestyle='--', label='Random', color='grey')
    
    roc_ax.set_title(f'ROC AUC = %.{float_precision}f'%roc_auc)
    roc_ax.set_xlabel('False Positive Rate (FPR)', fontsize=font_size)
    roc_ax.set_ylabel('True Positive Rate (TPR)', fontsize=font_size)
    roc_ax.legend(loc='lower right')
    roc_ax.grid(linewidth=0.5)
    
    
    # calculate precision-recall curve
    precision, recall, thresholds = precision_recall_curve(y_test, y_pred_prob[:, 1])#, pos_label=9)
    f1 = round(f1_score(y_true=y_true, y_pred=y_pred), float_precision)
    pr_auc = round(auc(recall, precision), float_precision)

    if return_thr_tables == True:
        threshold_table = list(zip(thresholds, precision, recall))
        pr_curve_df = pd.DataFrame(threshold_table, columns=['threshold', 'precision', 'recall']).sort_values(by='threshold', ascending=False)

    
    # draw Precision-Recall Curve
    pr_ax = ax[2]
    # calculate baseline accuracy accordingly to class balance
    random_prob = len(y_true[y_true==1]) / len(y_true)
    
    pr_ax.plot(recall, precision, marker='.', label='Model')
    pr_ax.plot([0, 1], [random_prob, random_prob], linestyle='--', color='grey', label='Random')

    pr_ax.set_title(f'PR AUC = {pr_auc}, F1 = {f1}')
    pr_ax.set_xlabel('Recall', fontsize=font_size)
    pr_ax.set_ylabel('Precision', fontsize=font_size)
    pr_ax.legend(loc='lower left')
    pr_ax.grid(linewidth=0.5)

    plt.show()
    
    if return_thr_tables == True:
        return roc_curve_df, pr_curve_df