import processing.video.*;
int minx, maxx, miny, maxy;
float grenzwert;
float offset;

Movie movie;

void setup() {
  background(255);
  //size(400, 400);
  fullScreen(1);
  frameRate(30);
  movie = new Movie(this, "video.mp4");
  movie.speed(0.125);
  movie.loop();
  minx = width;
  maxx = 0;
  miny = height;
  maxy = 0;
  grenzwert = 50;
  offset = 20;
  //frameRate(1);
}

void draw() {
  background(255);
  //tint(255, 100);
  //image(movie, mouseX, mouseY);
  //image(movie, 0, 0);
  movie.loadPixels();
  minx = movie.width;
  maxx = 0;
  miny = movie.height;
  maxy = 0;
  for (int i = 0; i < movie.height; i++) {
    for (int j = 0; j < movie.width; j++) {
      int pos = i * movie.width + j;
      int pix = movie.pixels[pos];
      float r = red(pix);
      float g = green(pix);
      float b = blue(pix);
      //float bw = (r + g + b)/3;
      if (r < grenzwert && g < grenzwert && b < grenzwert) {
        if (i < miny) {
          miny = i;
        }
        if (i > maxy) {
          maxy = i;
        }
        if (j < minx) {
          minx = j;
        }
        if (j > maxx) {
          maxx = j;
        }
        stroke(255, 0, 0, 100);
        strokeWeight(1);
        //point(j, i);
      }
    }
  }
  println(minx, miny, maxx, maxy);
  strokeWeight(1);
  stroke(255, 0, 0);
  fill(0, 10);
  rectMode(CORNERS);
  rect(minx - offset, miny - offset, maxx + offset, maxy + offset);
  strokeWeight(6);
  point(minx + (maxx - minx) / 2, miny + (maxy - miny) / 2);
  strokeWeight(3);
  stroke(255, 0, 0, 100);
  line(width / 2 - 50, height / 2, width / 2 + 50, height / 2);
  line(width / 2, height / 2 - 50, width / 2, height / 2 + 50);
  /*strokeWeight(10);
  //line(minx - offset, miny - offset, maxx + offset, miny - offset);
  point(minx - offset, miny - offset);
  stroke(255, 255, 0);
  //line(maxx + offset, miny - offset, maxx + offset, maxy + offset);
  point(maxx + offset, miny - offset);
  stroke(0, 255, 0);
  //line(maxx + offset, maxy + offset, minx - offset, maxy + offset);
  point(maxx + offset, maxy + offset);
  stroke(0, 255, 255);
  //line(minx - offset, maxy + offset, minx - offset, miny - offset);
  point(minx - offset, maxy + offset);*/
}

void movieEvent(Movie m) {
  m.read();
}
