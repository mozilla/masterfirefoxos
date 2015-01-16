var gulp = require('gulp');
var gulpFilter = require('gulp-filter');
var concat = require('gulp-concat');
var stylus = require('gulp-stylus');
var sourcemaps = require('gulp-sourcemaps');
var del = require('del');

var paths = {
  stylus: './masterfirefoxos/base/static/stylus',
  css: './masterfirefoxos/base/static/css/'
};

gulp.task('compress:base', function () {
  return gulp.src(paths.stylus + '/base.styl')
    .pipe(sourcemaps.init())
    .pipe(stylus({compress: true}))
    .pipe(concat('base.css'))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.css));
});

gulp.task('compress:home', function () {
  return gulp.src(paths.stylus + '/home.styl')
    .pipe(sourcemaps.init())
    .pipe(stylus({compress: true}))
    .pipe(concat('home.css'))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.css));
});

gulp.task('compress:ie', function () {
  return gulp.src(paths.stylus + '/oldIE.styl')
    .pipe(sourcemaps.init())
    .pipe(stylus({compress: true}))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.css));
});

gulp.task('clean:css', function (cb) {
  return del([
    paths.css + '/*',
    '!' + paths.css + '/README.md'
  ], cb);
});

gulp.task('default', ['clean:css', 'compress:base', 'compress:home', 'compress:ie']);




