package jtheiner.drawingclassification;



import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;


import java.util.ArrayList;

import jtheiner.drawingclassification.classification.ImageClassifier;


/**
 * Custom view class to draw sketches using bitmaps
 */
public class PaintView extends View {


    public static int BRUSH_SIZE = 50;
    public static final int DEFAULT_COLOR = Color.WHITE;
    public static final int DEFAULT_BG_COLOR = Color.BLACK;
    private static final float TOUCH_TOLERANCE = 4;

    // original size of PaintView
    public int WIDTH;
    public int HEIGHT;

    private float mX, mY;
    private Path mPath;
    private Paint mPaint;
    private ArrayList<PenPath> paths = new ArrayList<>();
    private Bitmap mBitmap;
    private Canvas mCanvas;
    private Paint mBitmapPaint = new Paint(Paint.DITHER_FLAG);

    public PaintView(Context context) {
        this(context, null);
    }

    public PaintView(Context context, AttributeSet attrs) {
        super(context, attrs);
        mPaint = new Paint();
        mPaint.setAntiAlias(true);
        mPaint.setDither(true);
        mPaint.setColor(DEFAULT_COLOR);
        mPaint.setStyle(Paint.Style.STROKE);
        mPaint.setStrokeJoin(Paint.Join.ROUND);
        mPaint.setStrokeCap(Paint.Cap.ROUND);
        mPaint.setXfermode(null);
        mPaint.setAlpha(0xff);
    }

    public void init() {
        this.WIDTH = this.getLayoutParams().width;
        this.HEIGHT = this.getLayoutParams().height;
        mBitmap = Bitmap.createBitmap(WIDTH, HEIGHT , Bitmap.Config.ARGB_8888);
        mCanvas = new Canvas(mBitmap);
    }

    public void clear() {
        paths.clear();
        invalidate();
    }

    @Override
    protected void onDraw(Canvas canvas) {
        canvas.save();
        mCanvas.drawColor(DEFAULT_BG_COLOR);

        for (PenPath fp : paths) {
            mPaint.setColor(fp.color);
            mPaint.setStrokeWidth(fp.strokeWidth);
            mPaint.setMaskFilter(null);
            mCanvas.drawPath(fp.path, mPaint);
        }

        canvas.drawBitmap(mBitmap, 0, 0, mBitmapPaint);
        canvas.restore();
    }

    private void touchStart(float x, float y) {
        mPath = new Path();
        PenPath fp = new PenPath(DEFAULT_COLOR, BRUSH_SIZE, mPath);
        paths.add(fp);
        mPath.reset();
        mPath.moveTo(x, y);
        mX = x;
        mY = y;
    }

    private void touchMove(float x, float y) {
        float dx = Math.abs(x - mX);
        float dy = Math.abs(y - mY);

        if (dx >= TOUCH_TOLERANCE || dy >= TOUCH_TOLERANCE) {
            mPath.quadTo(mX, mY, (x + mX) / 2, (y + mY) / 2);
            mX = x;
            mY = y;
        }
    }

    private void touchUp() {
        mPath.lineTo(mX, mY);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        float x = event.getX();
        float y = event.getY();

        switch(event.getAction()) {
            case MotionEvent.ACTION_DOWN :
                touchStart(x, y);
                invalidate();
                break;
            case MotionEvent.ACTION_MOVE :
                touchMove(x, y);
                invalidate();
                break;
            case MotionEvent.ACTION_UP :
                touchUp();
                invalidate();
                break;
        }

        return true;
    }

    public Bitmap getmBitmap() {
        return this.mBitmap;
    }

    // scale given bitmap by a factor and return a new bitmap
    public Bitmap scaleBitmap(int scaleFactor, Bitmap bitmap) {
        return Bitmap.createScaledBitmap(bitmap, (int)(bitmap.getWidth()*scaleFactor), (int)(bitmap.getHeight()*scaleFactor), true);
    }

    // scale original bitmap down to network size (28x28)
    public Bitmap getNormalizedBitmap() {
        float scaleFactor = ImageClassifier.DIM_IMG_SIZE_HEIGHT / (float) mBitmap.getHeight();
        // todo: cut empty space around sketch
        return Bitmap.createScaledBitmap(mBitmap, (int)(mBitmap.getWidth()*scaleFactor), (int)(mBitmap.getHeight()*scaleFactor), true);

    }

}