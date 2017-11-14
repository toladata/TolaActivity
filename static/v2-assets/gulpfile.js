let gulp        = require('gulp');
let cleanCSS = require('gulp-clean-css');
let autoprefixer = require('gulp-autoprefixer');
let browserSync = require('browser-sync').create();
let sass        = require('gulp-sass');
let concat = require('gulp-concat');
let cssmin = require('gulp-cssmin');
let reload      = browserSync.reload;

// Compile sass into CSS & auto-inject into browsers
gulp.task('sass', function () {
    return gulp.src('src/scss/**/*.scss')
        .pipe(sass())
        .on('error', function(err){
            console.error(err.message);
            browserSync.notify(err.message, 3000);
            this.emit('end');
        })
        .pipe(autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }))
        .pipe(cssmin())
        .pipe(gulp.dest('lib/css'))
        .pipe(gulp.dest("src/css"))
        .pipe(reload({stream:true}));
});


// Move the javascript files into our /src/js folder
gulp.task('js', function() {
    return gulp.src(['node_modules/bootstrap/dist/js/bootstrap.min.js', 'node_modules/jquery/dist/jquery.min.js', 'node_modules/tether/dist/js/tether.min.js'])
        .pipe(concat('script.js'))
        .pipe(gulp.dest("src/js"))
        .pipe(browserSync.stream());
});

// Static Server + watching scss/html files
gulp.task('serve', ['sass'], function() {

    browserSync.init({
        proxy: "http://127.0.0.1:8080/"
        //server: "./src"  
    });

    gulp.watch( 'src/scss/**/*.scss', ['sass']);
    gulp.watch("src/*.html").on('change', browserSync.reload);
});

gulp.task('default', ['js','serve']);