from .unet_2D import *
from .unet_3D import *
from .unet_nonlocal_2D import *
from .unet_nonlocal_3D import *
from .unet_grid_attention_3D import *
from .unet_pCT_multi_att_dsv_3D import *
from .unet_pCT_multi_att_dsv_25D_poolZ import *
from .unet_pCT_multi_att_dsv_25D_convZ import *


def get_network(name, n_classes, in_channels=3, input_nz=5, feature_scale=4, tensor_dim='3D',
                nonlocal_mode='embedded_gaussian', attention_dsample=(2,2,2),
                aggregation_mode='concat'):
    model = _get_model_instance(name, tensor_dim)

    if name in ['unet']:
        model = model(n_classes=n_classes,
                      is_batchnorm=True,
                      in_channels=in_channels,
                      feature_scale=feature_scale,
                      is_deconv=False)
    elif name in ['unet_nonlocal']:
        model = model(n_classes=n_classes,
                      is_batchnorm=True,
                      in_channels=in_channels,
                      is_deconv=False,
                      nonlocal_mode=nonlocal_mode,
                      feature_scale=feature_scale)
    elif name in ['unet_grid_gating', 'unet_pct_multi_att_dsv']:
        model = model(n_classes=n_classes,
                      is_batchnorm=True,
                      in_channels=in_channels,
                      nonlocal_mode=nonlocal_mode,
                      feature_scale=feature_scale,
                      attention_dsample=attention_dsample,
                      is_deconv=False)
    elif name in ['unet_pct_multi_att_dsv_25D_convZ', 'unet_pct_multi_att_dsv_25D_poolZ']:
        model = model(n_classes=n_classes,
                      is_batchnorm=True,
                      in_channels=in_channels,
                      nonlocal_mode=nonlocal_mode,
                      feature_scale=feature_scale,
                      attention_dsample=attention_dsample,
                      input_nz=input_nz,
                      is_deconv=False)
    else:
        raise 'Model {} not available'.format(name)

    return model


def _get_model_instance(name, tensor_dim):
    return {
        'unet':{'2D': unet_2D, '3D': unet_3D},
        'unet_nonlocal':{'2D': unet_nonlocal_2D, '3D': unet_nonlocal_3D},
        'unet_grid_gating': {'3D': unet_grid_attention_3D},
        'unet_pct_multi_att_dsv': {'3D': unet_pCT_multi_att_dsv_3D},
        'unet_pct_multi_att_dsv_25D_poolZ': {'3D': unet_pCT_multi_att_dsv_25D_poolZ},
        'unet_pct_multi_att_dsv_25D_convZ': {'3D': unet_pCT_multi_att_dsv_25D_convZ}
    }[name][tensor_dim]
