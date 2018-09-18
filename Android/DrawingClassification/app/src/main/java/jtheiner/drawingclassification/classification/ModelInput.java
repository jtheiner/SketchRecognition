package jtheiner.drawingclassification.classification;

import android.app.Activity;
import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.content.res.AssetManager;
import android.util.Log;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.Arrays;

import jtheiner.drawingclassification.MainActivity;


/**
 * Helper class to read TensorFlow model and labels from file
 */
abstract class ModelInput {

    /*
     * Reads the compressed model as MappedByteBuffer from file.
     *
     */
    public static MappedByteBuffer loadModelFile(Activity activity, String modelFile) throws IOException {
        AssetManager assetManager = activity.getAssets();
        AssetFileDescriptor fileDescriptor = assetManager.openFd(modelFile);
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }

    /*
     * Read labels from file to an array list of labels.
     * This list represents the mapping from index position to label.
     *
     */
    public static ArrayList readLabels(Activity activity, String labelsFile) {
        AssetManager assetManager = activity.getAssets();
        ArrayList<String> result = new ArrayList<>();
        try {
            InputStream is = assetManager.open(labelsFile);
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            String line;
            while ((line = br.readLine()) != null) {
                String[] splitted  = line.split(",");
                result.add(splitted[1]);
            }

            return result;
        } catch (IOException ex) {
            throw new IllegalStateException("Cannot read labels from " + labelsFile + " " + ex);
        }
    }
}
