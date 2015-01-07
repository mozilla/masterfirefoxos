var gulp = require('gulp');
var concat = require('gulp-concat');
var gulpFilter = require('gulp-filter');
var stylus = require('gulp-stylus');
var nib = require('nib');

gulp.task('compress-base', function () {
  var filter = gulpFilter(['*', '!oldIE.styl']);

  gulp.src('./masterfirefoxos/base/static/stylus/base.styl')
    .pipe(filter)
    .pipe(stylus({
      use: nib(),
      compress: true
    }))
    .pipe(concat('base.css'))
    .pipe(gulp.dest('./masterfirefoxos/base/static/css'));
});

gulp.task('compress-home', function () {
  var filter = gulpFilter(['*', '!oldIE.styl']);

  gulp.src('./masterfirefoxos/base/static/stylus/home.styl')
    .pipe(filter)
    .pipe(stylus({
      use: nib(),
      compress: true
    }))
    .pipe(concat('home.css'))
    .pipe(gulp.dest('./masterfirefoxos/base/static/css'));
});

gulp.task('compress-ie', function () {
  gulp.src('./masterfirefoxos/base/static/stylus/oldIE.styl')
    .pipe(stylus({
      use: nib(),
      compress: true
    }))
    .pipe(gulp.dest('./masterfirefoxos/base/static/css'));
});

gulp.task('compress', ['compress-base', 'compress-home', 'compress-ie']);

gulp.task('watch', ['compress'], function () {
  gulp.watch("./masterfirefoxos/base/static/stylus/**.styl", ['compress']);
});



