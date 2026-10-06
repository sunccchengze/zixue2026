
// Provide a default path to dwr.engine
if (dwr == null) var dwr = {};
if (dwr.engine == null) dwr.engine = {};
if (DWREngine == null) var DWREngine = dwr.engine;

if (PostBean == null) var PostBean = {};
PostBean._path = '/dwr';
PostBean.getAllPostsPagination = function(p0, p1, p2, p3, p4, p5, p6, callback) {
  dwr.engine._execute(PostBean._path, 'PostBean', 'getAllPostsPagination', p0, p1, p2, p3, p4, p5, p6, callback);
}
PostBean.getPostDetailById = function(p0, callback) {
  dwr.engine._execute(PostBean._path, 'PostBean', 'getPostDetailById', p0, callback);
}
PostBean.incrPostBrowse = function(p0, callback) {
  dwr.engine._execute(PostBean._path, 'PostBean', 'incrPostBrowse', p0, callback);
}
PostBean.getPaginationReplys = function(p0, p1, p2, callback) {
  dwr.engine._execute(PostBean._path, 'PostBean', 'getPaginationReplys', p0, p1, p2, callback);
}
PostBean.getPaginationComments = function(p0, p1, callback) {
  dwr.engine._execute(PostBean._path, 'PostBean', 'getPaginationComments', p0, p1, callback);
}
PostBean.getUserFollowedPosts = function(p0, p1, p2, p3, callback) {
  dwr.engine._execute(PostBean._path, 'PostBean', 'getUserFollowedPosts', p0, p1, p2, p3, callback);
}
PostBean.getRecommendPostByTermId = function(p0, callback) {
  dwr.engine._execute(PostBean._path, 'PostBean', 'getRecommendPostByTermId', p0, callback);
}
PostBean.getAllRecommendPost = function(callback) {
  dwr.engine._execute(PostBean._path, 'PostBean', 'getAllRecommendPost', callback);
}
PostBean.getRecommendPost = function(p0, callback) {
  dwr.engine._execute(PostBean._path, 'PostBean', 'getRecommendPost', p0, callback);
}
PostBean.clearUnreadCount = function(p0, p1, callback) {
  dwr.engine._execute(PostBean._path, 'PostBean', 'clearUnreadCount', p0, p1, callback);
}
