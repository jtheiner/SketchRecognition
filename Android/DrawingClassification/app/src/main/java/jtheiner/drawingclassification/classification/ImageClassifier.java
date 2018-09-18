package jtheiner.drawingclassification.classification;

import android.app.Activity;
import android.graphics.Bitmap;
import android.util.Log;

import org.tensorflow.lite.Interpreter;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.MappedByteBuffer;
import java.util.ArrayList;



public class ImageClassifier {

    private static final String MODEL_FILE = "100/model100.tflite";
    private static final String LABELS_FILE = "100/labels.csv";

    private static final int DIM_BATCH_SIZE = 1;
    public static final int DIM_IMG_SIZE_HEIGHT = 28;
    public static final int DIM_IMG_SIZE_WIDTH = 28;
    private static final int DIM_PIXEL_SIZE = 1;

    private ArrayList<String> labels; // list of all labels
    private ByteBuffer imgData = null; // models input format
    private Interpreter tflite; // the model
    private int[] imagePixels = new int[DIM_IMG_SIZE_HEIGHT * DIM_IMG_SIZE_WIDTH];
    private final float[][] result; // depending on models architecture (possible multiple output)

    private int expectedIndex; // random label index which is to be drawn

    public ImageClassifier(Activity activity) throws IOException {

        // load model
        MappedByteBuffer modelBuffered = ModelInput.loadModelFile(activity, MODEL_FILE);
        Log.i("ImageClassifier", "" + modelBuffered.isLoaded());
        this.tflite = new Interpreter(modelBuffered);

        // load labels
        this.labels = ModelInput.readLabels(activity, LABELS_FILE);
        this.result = new float[1][labels.size()];

        // allocate memory for model input
        this.imgData = ByteBuffer.allocateDirect(4 * DIM_BATCH_SIZE * DIM_IMG_SIZE_HEIGHT * DIM_IMG_SIZE_WIDTH * DIM_PIXEL_SIZE);
        this.imgData.order(ByteOrder.nativeOrder());

        Log.i("ImageClassifier", "Successfully created a Tensorflow Lite sketch classifier.");
    }

    public Result classify(Bitmap bitmap) {
        convertBitmapToByteBuffer(bitmap); // flatten bitmap to byte array
        tflite.run(imgData, result); // classify task
        return new Result(result[0], labels); // create the result
    }

    private void convertBitmapToByteBuffer(Bitmap bitmap) {
        if (imgData == null) {
            return;
        }
        imgData.rewind();

        bitmap.getPixels(imagePixels, 0, bitmap.getWidth(), 0, 0, bitmap.getWidth(), bitmap.getHeight());

        int pixel = 0;
        for (int i = 0; i < DIM_IMG_SIZE_WIDTH; ++i) {
            for (int j = 0; j < DIM_IMG_SIZE_HEIGHT; ++j) {
                final int color = imagePixels[pixel++];
                imgData.putFloat((((color >> 16) & 0xFF) + ((color >> 8) & 0xFF) + (color & 0xFF)) / 3.0f / 255.0f);
            }
        }
    }


    public void setExpectedIndex(int index) {
        this.expectedIndex = index;
    }


    public int getExpectedIndex() {
        return expectedIndex;
    }

    public float getProbability(int index) {
        return result[0][index];
    }

    public String getLabel(int index) {
        return labels.get(index);
    }

    public int getNumberOfClasses() {
        return labels.size();
    }
}
