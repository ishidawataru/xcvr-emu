# https://github.com/grpc/grpc/issues/37609#issuecomment-2328376837
import warnings
warnings.filterwarnings("ignore", "Protobuf gencode version", UserWarning, "google.protobuf.runtime_version")