
"""
Load frozen graph (.pb) and inspect tensors

"""

import tensorflow as tf


def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we can use again a convenient built-in function to import a graph_def into the
    # current default Graph
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(
            graph_def,
            input_map=None,
            return_elements=None,
            name="prefix",
            op_dict=None,
            producer_op_list=None
        )
    return graph


# ---------- settings -------------
graph = load_graph("model345.h5.pb") # model name
img_width = 28
img_height = 28
 

# access the list of operations in the graph
for op in graph.get_operations():
    print(op.name)

# access the input and output nodes
# default by tensorflow
x = graph.get_tensor_by_name('prefix/input_1:0')
y = graph.get_tensor_by_name('prefix/output_node0:0')

# launch the session and test whether random output returns the correct output shape
with tf.Session(graph=graph) as sess:

    import random
    img = [random.random()] * img_width*img_height
    import numpy as np
    img = np.array(img).reshape(img_width, img_height, 1)
    test_features = [img]
    # compute the predicted output for test_x
    pred_y = sess.run( y, feed_dict={x: test_features} )
    print(pred_y)
    print(pred_y.shape)
