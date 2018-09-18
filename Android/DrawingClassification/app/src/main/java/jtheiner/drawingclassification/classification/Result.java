package jtheiner.drawingclassification.classification;

import android.util.ArrayMap;
import android.util.Log;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * Readable representation of the models output vector.
 * Contains label, label position in result vector and probability.
 */
public class Result {
    private String label;
    private int labelPosition;
    private float probability;
    private List<Integer> topK; // contains the index

    public Result(float[] result, ArrayList<String> labels) {
        this.labelPosition = argmax(result); // set index position
        this.probability = result[labelPosition]; // set probability
        this.label = labels.get(labelPosition); // search for label
        this.topK = getTopkLabels(3, result);

    }

    // find the index with the maximum probability
    private int argmax(float[] result) {
        float maxProb = 0.0f;
        int maxIndex = -1;
        for (int i = 0; i < result.length; i++) {
            if (result[i] > maxProb) {
                maxProb = result[i];
                maxIndex = i;
            }
        }
        if (maxIndex == -1) {
            Log.e("Result class", "argmax found no maximum");
        }
        return maxIndex;
    }


    // returns the top k labels with probability
    private List<Integer> getTopkLabels(int k, float[] result) {
        List<Integer> topK = new LinkedList<>();
        for (int kk = 0; kk < k; kk++) {
            float maxProb = 0.0f;
            int maxIndex = -1;
            for (int i = 0; i < result.length; i++) {
                if (!topK.contains(i)) {
                    if (result[i] > maxProb) {
                        maxProb = result[i];
                        maxIndex = i;
                    }
                }
            }
            topK.add(maxIndex);
        }

        return topK;
    }

    public String getLabel() { return this.label; }

    public float getProbbability() {
        return this.probability;
    }

    public List<Integer> getTopK() {
        return this.topK;
    }

    public int getLabelPosition() {
        return this.labelPosition;
    }
}
