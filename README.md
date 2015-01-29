# LearnRelation

## Data Processing

## Single Relation Extraction

## Utility

## File Structure
* ProcData: code used for data preprocessing
* Single: code for single relation extraction
* Util: shared function for all code
* Data:
  * corpus: original data (xml)
  * sentence_t: sentence data in traditional Chinese (txt)
  * all_json: all data extracted from xml (json)

**All directories will be uploaded to github besides the Data folder**

## Data
###Categories
* all_category = ['人事', '心理', '訊息', '兒童文學', '財政', '災禍', '內政', '經濟', '民族文化', '政治現象', '影藝', '犯罪',  '環保', '食物', '社會現象', '宗教', '其他文學創作', '美術', '戲劇', '資訊', '教育', '語文', '軍事', '歷史', '工程', '體育',  '行銷', '交通運輸', '國家政策', '福利', '人物', '物理', '醫學', '商管', '俠義文學', '音樂', '休閒', '消費', '生物', '家庭',  '建築', '傳播', '衛生保健', '公益', '天文', '農漁牧業', '司法', '政治學', '技藝', '批評與鑑賞', '統計調查', '舞蹈', '思想',  '地理', '言情文學', '雕塑', '國際關係', '攝影', '文物', '藝術總論', '政黨', '電影', '衣飾', '鄉土', 文學', '文學通論', '考古', '社會學', '大氣科學', '數學', '礦冶', '化學']
###Format
* article
 * title
 * topic
 * sentences: list of sentences
  * a sentence is a list of (word, postag)
