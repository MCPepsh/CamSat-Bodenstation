import processing.video.*;

Movie movie;
PImage prev;

void setup() {
  background(255);
  //size(400, 400);
  fullScreen(2);
  frameRate(30);
  movie = new Movie(this, "video.mp4");
  movie.speed(0.125);
  movie.loop();
  prev = movie;
  //frameRate(1);
}

void draw() {
  movie.loadPixels();
  prev.loadPixels();
  for (int x = 0; x < movie.width; x++) {
    for (int y = 0; y < movie.height; y++) {
      int pos = x * movie.height + y;
      int pix = movie.pixels[pos];
      float r = abs(red(pix)   - red(pix)  );
      float g = abs(green(pix) - green(pix));
      float b = abs(blue(pix)  - blue(pix) );
      stroke(r, g, b);
      point(x, y);
    }
  }
  prev = movie;
}

void movieEvent(Movie m) {
  m.read();
}
