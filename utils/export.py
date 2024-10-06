""" # Assume your PyTorch model is called `pytorch_model`
# dummy_input = torch.randn(1, 108)  # Replace `input_size` with your model's input size
import onnx
from onnx_tf.backend import prepare
onnx_model = onnx.load("model.onnx")
tf_rep = prepare(onnx_model)
tf_rep.export_graph("model.pb") """