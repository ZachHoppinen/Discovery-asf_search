from asf_search import ASFSession, ASFProduct
from asf_search.CMR.translate import get as umm_get, cast as umm_cast
# offnadir
# faradayRotation
# 'faradayRotation': cast(float, get(umm, 'AdditionalAttributes', ('Name', 'FARADAY_ROTATION'), 'Values', 0)),
#     'offNadirAngle': cast(float, get(umm, 'AdditionalAttributes', ('Name', 'OFF_NADIR_ANGLE'), 'Values', 0)),

class RadarsatProduct(ASFProduct):
    base_properties = {
        'browse'
        'faradayRotation',
        'offNadirAngle',
        'insarStackId',
        'processingDate',
        'sceneName',
        'orbit',
        'polarization',
        'md5sum',
        'sensor',
        'bytes',
        'granuleType',
        'frameNumber'
    }
    
    def __init__(self, args: dict = {}, session: ASFSession = ASFSession()):
        super().__init__(args, session)
        self.baseline = self.get_baseline_calc_properties()
    
    def get_baseline_calc_properties(self) -> dict:
        insarBaseline = umm_cast(float, umm_get(self.umm, 'AdditionalAttributes', ('Name', 'INSAR_BASELINE'), 'Values', 0))
        
        if insarBaseline is not None:
            return {
                'insarBaseline': insarBaseline        
            }
        
        return None

    @staticmethod
    def _get_property_paths() -> dict:
        return {
            **ASFProduct._get_property_paths(),
            **RadarsatProduct.base_properties
        }
    
    def get_default_product_type(self):
        # if get_platform(scene_name) in ['R1', 'E1', 'E2', 'J1']:
        return 'L0'