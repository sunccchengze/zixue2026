
// Provide a default path to dwr.engine
if (dwr == null) var dwr = {};
if (dwr.engine == null) dwr.engine = {};
if (DWREngine == null) var DWREngine = dwr.engine;

if (CourseBean == null) var CourseBean = {};
CourseBean._path = '/dwr';
CourseBean.checkParameterInvalid = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'checkParameterInvalid', p0, callback);
}
CourseBean.getMocCourseList = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getMocCourseList', p0, callback);
}
CourseBean.getMocCourseDtoStatistic = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getMocCourseDtoStatistic', p0, callback);
}
CourseBean.startTermLearn = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'startTermLearn', p0, p1, callback);
}
CourseBean.getEnrollCountByCourseIds = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getEnrollCountByCourseIds', p0, callback);
}
CourseBean.getLessonUnitLearnVo = function(p0, p1, p2, p3, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getLessonUnitLearnVo', p0, p1, p2, p3, callback);
}
CourseBean.getCoursePanelListBySchoolId = function(p0, p1, p2, p3, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getCoursePanelListBySchoolId', p0, p1, p2, p3, callback);
}
CourseBean.getMyLearnedCoursePanelList = function(p0, p1, p2, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getMyLearnedCoursePanelList', p0, p1, p2, callback);
}
CourseBean.canDeleteTermLearnRecord4Spoc = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'canDeleteTermLearnRecord4Spoc', p0, callback);
}
CourseBean.validateTermPassword = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'validateTermPassword', p0, p1, callback);
}
CourseBean.getAllCoursePanelListByStaffId = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getAllCoursePanelListByStaffId', p0, p1, callback);
}
CourseBean.getCategorys = function(callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getCategorys', callback);
}
CourseBean.getCoursePanelListByCategory = function(p0, p1, p2, p3, p4, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getCoursePanelListByCategory', p0, p1, p2, p3, p4, callback);
}
CourseBean.saveMocContentLearn = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'saveMocContentLearn', p0, callback);
}
CourseBean.getMocTermDto = function(p0, p1, p2, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getMocTermDto', p0, p1, p2, callback);
}
CourseBean.checkTermLearn = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'checkTermLearn', p0, callback);
}
CourseBean.getLessonUnitPreviewVo = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getLessonUnitPreviewVo', p0, p1, callback);
}
CourseBean.getCoursePanelListForPlatform = function(p0, p1, p2, p3, p4, p5, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getCoursePanelListForPlatform', p0, p1, p2, p3, p4, p5, callback);
}
CourseBean.getEditorList = function(callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getEditorList', callback);
}
CourseBean.getCoursePanelListForSchoolAdmin = function(p0, p1, p2, p3, p4, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getCoursePanelListForSchoolAdmin', p0, p1, p2, p3, p4, callback);
}
CourseBean.setOrdinaryEditorForCourse = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'setOrdinaryEditorForCourse', p0, p1, callback);
}
CourseBean.deleteOrdinaryEditorForCourse = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'deleteOrdinaryEditorForCourse', p0, p1, callback);
}
CourseBean.getRadomCoursePanelList = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getRadomCoursePanelList', p0, callback);
}
CourseBean.getVisibleLearnCustomMenuItems = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getVisibleLearnCustomMenuItems', p0, p1, callback);
}
CourseBean.getMocTermDtoFromDraft = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getMocTermDtoFromDraft', p0, p1, callback);
}
CourseBean.getMocTermDtoForSpocTerm = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getMocTermDtoForSpocTerm', p0, callback);
}
CourseBean.getLastLearnedMocTermDto = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getLastLearnedMocTermDto', p0, callback);
}
CourseBean.getNextLessonUnit = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getNextLessonUnit', p0, callback);
}
CourseBean.getNextVideo = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getNextVideo', p0, callback);
}
CourseBean.getLessonInfo = function(p0, p1, p2, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getLessonInfo', p0, p1, p2, callback);
}
CourseBean.getLessonInfoAndFilter = function(p0, p1, p2, p3, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getLessonInfoAndFilter', p0, p1, p2, p3, callback);
}
CourseBean.deleteTermLearn = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'deleteTermLearn', p0, callback);
}
CourseBean.getAllAnnouncementByTerm = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getAllAnnouncementByTerm', p0, p1, callback);
}
CourseBean.getMixedForumAnnouncementByTerm = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getMixedForumAnnouncementByTerm', p0, p1, callback);
}
CourseBean.getCourseByIds = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getCourseByIds', p0, callback);
}
CourseBean.getMocCourseDto = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getMocCourseDto', p0, callback);
}
CourseBean.getLessonUnitLearnVoFromDraft = function(p0, p1, p2, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getLessonUnitLearnVoFromDraft', p0, p1, p2, callback);
}
CourseBean.getEvaluationDescription = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getEvaluationDescription', p0, p1, callback);
}
CourseBean.getCategorysAddCAP = function(callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getCategorysAddCAP', callback);
}
CourseBean.getScholarshipCategorys = function(callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getScholarshipCategorys', callback);
}
CourseBean.getCategorysByType = function(p0, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getCategorysByType', p0, callback);
}
CourseBean.getCoursePanelListByCategoryIds = function(p0, p1, p2, p3, p4, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getCoursePanelListByCategoryIds', p0, p1, p2, p3, p4, callback);
}
CourseBean.getCAPCoursePanelList = function(p0, p1, p2, p3, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getCAPCoursePanelList', p0, p1, p2, p3, callback);
}
CourseBean.getVocationalCourseList = function(p0, p1, p2, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getVocationalCourseList', p0, p1, p2, callback);
}
CourseBean.changeCourseChannelById = function(p0, p1, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'changeCourseChannelById', p0, p1, callback);
}
CourseBean.getTermPanelListForPlatform = function(p0, p1, p2, p3, p4, p5, p6, p7, p8, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getTermPanelListForPlatform', p0, p1, p2, p3, p4, p5, p6, p7, p8, callback);
}
CourseBean.getTermPanelListForFromCourse = function(p0, p1, p2, p3, p4, p5, p6, p7, p8, callback) {
  dwr.engine._execute(CourseBean._path, 'CourseBean', 'getTermPanelListForFromCourse', p0, p1, p2, p3, p4, p5, p6, p7, p8, callback);
}
