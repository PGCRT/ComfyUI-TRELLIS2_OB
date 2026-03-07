"""ComfyUI-TRELLIS2 Nodes."""

# Compatibility shim: flex_gemm was renamed from flex_gemm_ap in v1.0.
# comfy-sparse-attn (PyPI) still imports flex_gemm_ap; register aliases in
# sys.modules so both detect.py and ops_sparse.py find the right package.
# This is a no-op in the main ComfyUI process (flex_gemm not on its path).
try:
    import sys as _sys
    import flex_gemm as _fg
    import flex_gemm.ops as _fg_ops
    import flex_gemm.ops.spconv as _fg_spconv
    import flex_gemm.ops.spconv.submanifold_conv3d as _fg_subm
    for _old, _new in [
        ("flex_gemm_ap",                                  _fg),
        ("flex_gemm_ap.ops",                              _fg_ops),
        ("flex_gemm_ap.ops.spconv",                       _fg_spconv),
        ("flex_gemm_ap.ops.spconv.submanifold_conv3d",    _fg_subm),
    ]:
        _sys.modules.setdefault(_old, _new)
    del _sys, _fg, _fg_ops, _fg_spconv, _fg_subm, _old, _new
except ImportError:
    pass  # Main ComfyUI process — flex_gemm lives only in the pixi env

# Stage sparse primitives under the comfy namespace so that model code can
# import from comfy.sparse / comfy.ops_sparse / comfy.attention_sparse as if
# the upstream PR were already merged.  setup_link is a no-op when ComfyUI
# already ships those files as real (non-symlink) files.
import pathlib
import comfy_sparse_attn
from comfy_sparse_attn import setup_link
_PKG = pathlib.Path(comfy_sparse_attn.__file__).parent
setup_link(_PKG / "sparse.py",           "sparse.py")
setup_link(_PKG / "ops_sparse.py",       "ops_sparse.py")
setup_link(_PKG / "attention_sparse.py", "attention_sparse.py")
del pathlib, comfy_sparse_attn, setup_link, _PKG

from .nodes_loader import NODE_CLASS_MAPPINGS as loader_mappings
from .nodes_loader import NODE_DISPLAY_NAME_MAPPINGS as loader_display
from .nodes_export import NODE_CLASS_MAPPINGS as export_mappings
from .nodes_export import NODE_DISPLAY_NAME_MAPPINGS as export_display
from .nodes_unwrap import NODE_CLASS_MAPPINGS as unwrap_mappings
from .nodes_unwrap import NODE_DISPLAY_NAME_MAPPINGS as unwrap_display
from .nodes_inference import NODE_CLASS_MAPPINGS as inference_mappings
from .nodes_inference import NODE_DISPLAY_NAME_MAPPINGS as inference_display
from .nodes_native_sampling import NODE_CLASS_MAPPINGS as native_mappings
from .nodes_native_sampling import NODE_DISPLAY_NAME_MAPPINGS as native_display

NODE_CLASS_MAPPINGS = {
    **loader_mappings,
    **export_mappings,
    **unwrap_mappings,
    **inference_mappings,
    **native_mappings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **loader_display,
    **export_display,
    **unwrap_display,
    **inference_display,
    **native_display,
}
