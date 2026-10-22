
// Provide a default path to dwr.engine
if (dwr == null) var dwr = {};
if (dwr.engine == null) dwr.engine = {};
if (DWREngine == null) var DWREngine = dwr.engine;

if (MocQuizBean == null) var MocQuizBean = {};
MocQuizBean._path = '/dwr';
MocQuizBean.getQuizInfo = function(p0, p1, p2, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'getQuizInfo', p0, p1, p2, callback);
}
MocQuizBean.getHomeworkInfo = function(p0, p1, p2, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'getHomeworkInfo', p0, p1, p2, callback);
}
MocQuizBean.getHomeworkPaperDto = function(p0, p1, p2, p3, p4, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'getHomeworkPaperDto', p0, p1, p2, p3, p4, callback);
}
MocQuizBean.deleteAttachment = function(p0, p1, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'deleteAttachment', p0, p1, callback);
}
MocQuizBean.getOpenQuizInfo = function(p0, p1, p2, p3, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'getOpenQuizInfo', p0, p1, p2, p3, callback);
}
MocQuizBean.saveDraftAnswers = function(p0, p1, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'saveDraftAnswers', p0, p1, callback);
}
MocQuizBean.submitAnswers = function(p0, p1, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'submitAnswers', p0, p1, callback);
}
MocQuizBean.getOpenHomeworkInfo = function(p0, p1, p2, p3, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'getOpenHomeworkInfo', p0, p1, p2, p3, callback);
}
MocQuizBean.getHomeworkEvalInfo = function(p0, p1, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'getHomeworkEvalInfo', p0, p1, callback);
}
MocQuizBean.getOpenQuizPaperDto = function(p0, p1, p2, p3, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'getOpenQuizPaperDto', p0, p1, p2, p3, callback);
}
MocQuizBean.getOpenHomeworkPaperDto = function(p0, p1, p2, p3, p4, p5, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'getOpenHomeworkPaperDto', p0, p1, p2, p3, p4, p5, callback);
}
MocQuizBean.fetchQuestions = function(p0, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'fetchQuestions', p0, callback);
}
MocQuizBean.getQuizPaperDto = function(p0, p1, p2, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'getQuizPaperDto', p0, p1, p2, callback);
}
MocQuizBean.deleteQuestionTitleAttachment = function(p0, p1, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'deleteQuestionTitleAttachment', p0, p1, callback);
}
MocQuizBean.deleteQuestionTitleAttachmentDraft = function(p0, p1, p2, callback) {
  dwr.engine._execute(MocQuizBean._path, 'MocQuizBean', 'deleteQuestionTitleAttachmentDraft', p0, p1, p2, callback);
}
