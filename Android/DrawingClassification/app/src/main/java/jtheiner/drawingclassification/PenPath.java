package jtheiner.drawingclassification;

import android.graphics.Path;

public class PenPath {

    public int color;
    public int strokeWidth;
    public Path path;

    public PenPath(int color, int strokeWidth, Path path) {
        this.color = color;
        this.strokeWidth = strokeWidth;
        this.path = path;
    }
}