from typing import Any
from ipkiss.process import PatternPurpose, ProcessPurposeLayer, ProcessLayer
from ipkiss.technology.technology import ProcessTechnologyTree
from ipkiss.technology.technology import TechnologyLibrary
from ipkiss.technology.technology import TechnologyTree

class TechnologyTreeWIREWG(TechnologyTree):
    ANGLE_STEP: float
    BEND_RADIUS: float
    CLADDING_WIDTH: float
    DC_SPACING: float
    EXPANDED_STRAIGHT: float
    EXPANDED_TAPER_LENGTH: float
    EXPANDED_WIDTH: float
    OVERLAP_EXTENSION: float
    OVERLAP_TRENCH: float
    SHORT_STRAIGHT: float
    SHORT_TAPER_LENGTH: float
    SHORT_TRANSITION_LENGTH: float
    SLOTTED_WIRE_WIDTH: float
    SLOT_WIDTH: float
    SPACING: float
    TRENCH_WIDTH: float
    WIRE_WIDTH: float

class TechnologyTreeWG_DEFAULTS(TechnologyTree):
    CORE_LAYER: ProcessPurposeLayer
    LOSS_DB_PERM: float
    N_EFF: float
    N_GROUP: float

class TechnologyTreeWG1(TechnologyTree):
    ANGLE_STEP: float
    BEND_RADIUS: float
    CLADDING_WIDTH: float
    DC_SPACING: float
    EXPANDED_STRAIGHT: float
    EXPANDED_TAPER_LENGTH: float
    EXPANDED_WIDTH: float
    OVERLAP_EXTENSION: float
    OVERLAP_TRENCH: float
    SHORT_STRAIGHT: float
    SHORT_TAPER_LENGTH: float
    SHORT_TRANSITION_LENGTH: float
    SLOTTED_WIRE_WIDTH: float
    SLOT_WIDTH: float
    SPACING: float
    TRENCH_WIDTH: float
    WIRE_WIDTH: float

class TechnologyTreeV120(TechnologyTree):
    M1_WIDTH: float
    M2_WIDTH: float
    N_O_SIDES: int
    VIA_WIDTH: float

class TechnologyTreeDEFAULT0(TechnologyTree):
    BOTTOM_SHAPE: Any
    TOP_SHAPE: Any
    VIA_SHAPE: Any

class TechnologyTreeCONTACT_HOLE(TechnologyTree):
    M1_WIDTH: float
    SIL_WIDTH: float
    VIA_WIDTH: float

class TechnologyTreeVIAS(TechnologyTree):
    CONTACT_HOLE: TechnologyTreeCONTACT_HOLE
    DEFAULT: TechnologyTreeDEFAULT0
    V12: TechnologyTreeV120

class TechnologyTreeVFABRICATION(TechnologyTree):
    PROCESS_FLOW: Any
    PROCESS_FLOW_BEOL_M1: Any
    PROCESS_FLOW_BEOL_M2: Any
    PROCESS_FLOW_FEOL: Any

class TechnologyTreeV12(TechnologyTree):
    BOTTOM_SHAPE: Any
    DEFAULT_VIA_PITCH: tuple
    TOP_SHAPE: Any
    VIA_SHAPE: Any
    WIDTH: float

class TechnologyTreeTRACE(TechnologyTree):
    BEND_RADIUS: float
    CONTROL_SHAPE_LAYER: ProcessPurposeLayer
    DEFAULT_LAYER: ProcessPurposeLayer
    DRAW_CONTROL_SHAPE: bool

class TechnologyTreeTECH(TechnologyTree):
    MINIMUM_LINE: float
    MINIMUM_SPACE: float

class TechnologyTreeSK(TechnologyTree):
    CLADDING_WIDTH: float

class TechnologyTreeSINWG(TechnologyTree):
    BEND_RADIUS: float
    CLADDING_WIDTH: float
    SPACING: float
    TRENCH_WIDTH: float
    WIRE_WIDTH: float

class TechnologyTreeRWG(TechnologyTree):
    BEND_RADIUS: float
    CLADDING_WIDTH: float
    RIB_WIDTH: float
    SPACING: float
    STRIP_WIDTH: float
    TRENCH_WIDTH: float
    WIRE_WIDTH: float

class TechnologyTreeROUTING(TechnologyTree):
    WAVEGUIDE_GENERATION_GUIDE_LAYERS: dict

class TechnologyTreeRIBWG(TechnologyTree):
    BEND_RADIUS: float
    CLADDING_WIDTH: float
    RIB_WIDTH: float
    SPACING: float
    STRIP_WIDTH: float
    TRENCH_WIDTH: float
    WIRE_WIDTH: float

class TechnologyTreeLF(TechnologyTree):
    LINE: PatternPurpose

class TechnologyTreeDF(TechnologyTree):
    LINE: PatternPurpose
    POLYGON: PatternPurpose

class TechnologyTreePURPOSE(TechnologyTree):
    BBOX: PatternPurpose
    DEVREC: PatternPurpose
    DF: TechnologyTreeDF
    DF_AREA: PatternPurpose
    DOC: PatternPurpose
    DRAWING: PatternPurpose
    DRWSUB: PatternPurpose
    ERROR: PatternPurpose
    IGNORE: PatternPurpose
    LF: TechnologyTreeLF
    LF_AREA: PatternPurpose
    PINREC: PatternPurpose
    SIMBND: PatternPurpose
    TEXT: PatternPurpose
    TRACE: PatternPurpose
    UNUSED: PatternPurpose

class ProcessTechnologyTreePROCESS(ProcessTechnologyTree):
    BEZ_B: ProcessLayer
    BEZ_S: ProcessLayer
    BEZ_U: ProcessLayer
    CON: ProcessLayer
    FC: ProcessLayer
    GE: ProcessLayer
    HFW: ProcessLayer
    HT: ProcessLayer
    M1: ProcessLayer
    M2: ProcessLayer
    N: ProcessLayer
    NONE: ProcessLayer
    NPLUS: ProcessLayer
    P: ProcessLayer
    PPLUS: ProcessLayer
    RWG: ProcessLayer
    SB: ProcessLayer
    SHALLOW: ProcessLayer
    SI: ProcessLayer
    SIL: ProcessLayer
    SIN: ProcessLayer
    SIN_SHALLOW: ProcessLayer
    SK: ProcessLayer
    V12: ProcessLayer
    WG: ProcessLayer

class TechnologyTreeWG0(TechnologyTree):
    TEXT: ProcessPurposeLayer

class TechnologyTreeERROR(TechnologyTree):
    CROSSING: ProcessPurposeLayer
    GENERIC: ProcessPurposeLayer

class TechnologyTreePPLAYER(TechnologyTree):
    BEZ_B: ProcessPurposeLayer
    BEZ_S: ProcessPurposeLayer
    BEZ_U: ProcessPurposeLayer
    CON: ProcessPurposeLayer
    DOC: ProcessPurposeLayer
    ERROR: TechnologyTreeERROR
    GE: ProcessPurposeLayer
    HT: ProcessPurposeLayer
    M1: ProcessPurposeLayer
    M2: ProcessPurposeLayer
    N: ProcessPurposeLayer
    NONE: ProcessPurposeLayer
    NPLUS: ProcessPurposeLayer
    P: ProcessPurposeLayer
    PINREC: ProcessPurposeLayer
    PPLUS: ProcessPurposeLayer
    RIB_TRACE: ProcessPurposeLayer
    SB: ProcessPurposeLayer
    SHALLOW: ProcessPurposeLayer
    SHALLOW_TRENCH: ProcessPurposeLayer
    SI: ProcessPurposeLayer
    SIN: ProcessPurposeLayer
    SIN_CLADDING: ProcessPurposeLayer
    SIN_SHALLOW: ProcessPurposeLayer
    SIN_SHALLOW_TRENCH: ProcessPurposeLayer
    SI_CLADDING: ProcessPurposeLayer
    SI_TRENCH: ProcessPurposeLayer
    TEXT: ProcessPurposeLayer
    V12: ProcessPurposeLayer
    WG: TechnologyTreeWG0
    WIRE_TRACE: ProcessPurposeLayer

class TechnologyTreePORT(TechnologyTree):
    DEFAULT_LAYER: ProcessPurposeLayer
    DEFAULT_LENGTH: float

class TechnologyTreeWG(TechnologyTree):
    DEFAULT: Any
    RIB: Any
    RIBWIRE: Any
    WIRE: Any

class TechnologyTreeTRANSITION(TechnologyTree):
    AUTO_TRANSITION_DATABASE: Any

class TechnologyTreeMETAL0(TechnologyTree):
    DEFAULT: Any
    WIRE: Any

class TechnologyTreePCELLS2(TechnologyTree):
    LIB: Any
    METAL: TechnologyTreeMETAL0
    TRANSITION: TechnologyTreeTRANSITION
    WG: TechnologyTreeWG

class TechnologyTreeOPENACCESS(TechnologyTree):
    EXPORT_LAYER_MAP: Any
    EXPORT_PURPOSE_MAP: Any
    FILTER: Any

class TechnologyTreePN(TechnologyTree):
    JUNCTION_OVERLAP: float
    NPLUS_EXTENSION: float
    NPLUS_OFFSET: float
    NPLUS_WIDTH: float
    N_CONT_OFFSETS: list
    N_CONT_PITCH: float
    N_METAL1_OFFSET: float
    N_METAL1_WIDTH: float
    N_SIL_EXTENSION: float
    N_SIL_OFFSET: float
    N_SIL_WIDTH: float
    N_WIDTH: float
    PPLUS_EXTENSION: float
    PPLUS_OFFSET: float
    PPLUS_WIDTH: float
    P_CONT_OFFSETS: list
    P_CONT_PITCH: float
    P_METAL1_OFFSET: float
    P_METAL1_WIDTH: float
    P_SIL_EXTENSION: float
    P_SIL_OFFSET: float
    P_SIL_WIDTH: float
    P_WIDTH: float

class TechnologyTreeLONGPN(TechnologyTree):
    N_LENGTH: float
    N_WIDTH: float
    P_LENGTH: float
    P_WIDTH: float

class TechnologyTreeLATPN(TechnologyTree):
    BRIDGE_PITCH: float
    BRIDGE_WIDTH: float
    JUNCTION_OFFSET: float

class TechnologyTreePHASESHIFTER(TechnologyTree):
    LATPN: TechnologyTreeLATPN
    LONGPN: TechnologyTreeLONGPN
    PN: TechnologyTreePN

class TechnologyTreeMODULATORS(TechnologyTree):
    PHASESHIFTER: TechnologyTreePHASESHIFTER

class TechnologyTreeMETRICS(TechnologyTree):
    ANGLE_STEP: float
    GRID: float
    UNIT: float

class TechnologyTreeMETAL(TechnologyTree):
    DEFAULT_PROCESS: ProcessLayer
    LINE_WIDTH: float

class TechnologyTreeMASK(TechnologyTree):
    POLARITY_DF: str
    POLARITY_LF: str

class TechnologyTreeM2(TechnologyTree):
    LINE_WIDTH: float

class TechnologyTreeM1(TechnologyTree):
    LINE_WIDTH: float

class TechnologyTreeSOCKET1(TechnologyTree):
    LENGTH: float
    TRACE_TEMPLATE: Any

class TechnologyTreePCELLS1(TechnologyTree):
    DEFAULT_GRATING: Any
    DEFAULT_GRATING_TE: Any
    DEFAULT_GRATING_TM: Any

class TechnologyTreeGRATING_TM(TechnologyTree):
    BOX_WIDTH: float
    LINE_WIDTH: float
    N_O_LINES: int
    PERIOD: float

class TechnologyTreeGRATING_TE(TechnologyTree):
    BOX_WIDTH: float
    LINE_WIDTH: float
    N_O_LINES: int
    PERIOD: float

class TechnologyTreeGRATING1(TechnologyTree):
    BOX_WIDTH: float
    LINE_WIDTH: float
    N_O_LINES: int
    PERIOD: float

class TechnologyTreeSTRAIGHT(TechnologyTree):
    GRATING: TechnologyTreeGRATING1
    GRATING_TE: TechnologyTreeGRATING_TE
    GRATING_TM: TechnologyTreeGRATING_TM
    PCELLS: TechnologyTreePCELLS1
    SOCKET: TechnologyTreeSOCKET1

class TechnologyTreeSOCKET0(TechnologyTree):
    LENGTH: float
    MARGIN_FROM_GRATING: float
    START_TRACE_TEMPLATE: Any
    STRAIGHT_EXTENSION: list
    WIDE_TRACE_TEMPLATE: Any

class TechnologyTreePCELLS0(TechnologyTree):
    DEFAULT_GRATING: Any

class TechnologyTreeGRATING0(TechnologyTree):
    ANGLE_SPAN: int
    BOX_WIDTH: float
    FOCAL_DISTANCE: float
    N_O_LINES: int
    PERIOD: float
    START_RADIUS: float

class TechnologyTreeDEFAULT(TechnologyTree):
    GRATING: TechnologyTreeGRATING0
    PCELLS: TechnologyTreePCELLS0
    SOCKET: TechnologyTreeSOCKET0

class TechnologyTreeSOCKET(TechnologyTree):
    LENGTH: float
    MARGIN_FROM_GRATING: float
    START_TRACE_TEMPLATE: Any
    STRAIGHT_EXTENSION: list
    WIDE_TRACE_TEMPLATE: Any

class TechnologyTreePCELLS(TechnologyTree):
    DEFAULT_GRATING: Any

class TechnologyTreeGRATING(TechnologyTree):
    ANGLE_SPAN: int
    BOX_WIDTH: float
    FOCAL_DISTANCE: float
    N_O_LINES: int
    PERIOD: float
    START_RADIUS: float

class TechnologyTreeCURVED(TechnologyTree):
    GRATING: TechnologyTreeGRATING
    PCELLS: TechnologyTreePCELLS
    SOCKET: TechnologyTreeSOCKET

class TechnologyTreeFIBCOUP(TechnologyTree):
    CURVED: TechnologyTreeCURVED
    DEFAULT: TechnologyTreeDEFAULT
    STRAIGHT: TechnologyTreeSTRAIGHT

class TechnologyTreeIOFIBCOUP(TechnologyTree):
    CONNECT_TRANSITION_LENGTH: Any
    FANOUT_LENGTH: float
    FIBER_COUPLER_TRANSITION_LENGTH: Any
    S_BEND_ANGLE: float

class TechnologyTreeDEFAULT_ADAPTER(TechnologyTree):
    ADAPTER: Any

class TechnologyTreeADAPTER(TechnologyTree):
    DEFAULT_ADAPTER: TechnologyTreeDEFAULT_ADAPTER
    IOFIBCOUP: TechnologyTreeIOFIBCOUP

class TechnologyTreeIO(TechnologyTree):
    ADAPTER: TechnologyTreeADAPTER
    FIBCOUP: TechnologyTreeFIBCOUP

class TechnologyTreeGDSII(TechnologyTree):
    EXPORT_LAYER_MAP: Any
    FILTER: Any
    IMPORT_LAYER_MAP: Any
    LAYERTABLE: dict
    MAX_COORDINATES: int
    MAX_NAME_LENGTH: int
    MAX_PATH_LENGTH: int
    MAX_VERTEX_COUNT: int
    NAME_FILTER: Any
    STRNAME_ALLOWED_CHARACTERS: str
    STRNAME_CHARACTER_DICT: dict

class TechnologyTreeDUMMY_FILLING(TechnologyTree):
    FILLERS: list
    TARGET_LAYER: Any

class TechnologyTreePREDEFINED_STYLE_SETS(TechnologyTree):
    CYCLIC: Any

class TechnologyTreeDISPLAY(TechnologyTree):
    DEFAULT_DISPLAY_STYLE_SET: Any
    PREDEFINED_STYLE_SETS: TechnologyTreePREDEFINED_STYLE_SETS

class TechnologyTreeTERMINATE_PORTS(TechnologyTree):
    CHILD_SUFFIX: str
    TERMINATION_INSTANCE_PREFIX: str

class TechnologyTreeCONTAINER(TechnologyTree):
    TERMINATE_PORTS: TechnologyTreeTERMINATE_PORTS

class TechnologyTreeCON(TechnologyTree):
    WIDTH: float

class TechnologyTreeBONDPAD(TechnologyTree):
    M1_SIZE: tuple
    M2_SIZE: tuple
    VIA_PITCH: tuple

class TechnologyTreeBLOCKS(TechnologyTree):
    DEFAULT_WIDTH: float
    DEFAULT_YSPACING: float

class TechnologyTreeADMIN(TechnologyTree):
    NAME_GENERATOR: Any

class PteamLibrarySiFabTechnologyLibrary(TechnologyLibrary):
    ADMIN: TechnologyTreeADMIN
    BLOCKS: TechnologyTreeBLOCKS
    BONDPAD: TechnologyTreeBONDPAD
    CON: TechnologyTreeCON
    CONTAINER: TechnologyTreeCONTAINER
    DEFAULT_WAVELENGTH: float
    DISPLAY: TechnologyTreeDISPLAY
    DUMMY_FILLING: TechnologyTreeDUMMY_FILLING
    GDSII: TechnologyTreeGDSII
    IO: TechnologyTreeIO
    M1: TechnologyTreeM1
    M2: TechnologyTreeM2
    MASK: TechnologyTreeMASK
    MATERIALS: Any
    MATERIAL_STACKS: Any
    METAL: TechnologyTreeMETAL
    METRICS: TechnologyTreeMETRICS
    MODULATORS: TechnologyTreeMODULATORS
    OPENACCESS: TechnologyTreeOPENACCESS
    PCELLS: TechnologyTreePCELLS2
    PORT: TechnologyTreePORT
    PPLAYER: TechnologyTreePPLAYER
    PROCESS: ProcessTechnologyTreePROCESS
    PURPOSE: TechnologyTreePURPOSE
    RIBWG: TechnologyTreeRIBWG
    ROUTING: TechnologyTreeROUTING
    RWG: TechnologyTreeRWG
    SINWG: TechnologyTreeSINWG
    SK: TechnologyTreeSK
    TECH: TechnologyTreeTECH
    TRACE: TechnologyTreeTRACE
    V12: TechnologyTreeV12
    VFABRICATION: TechnologyTreeVFABRICATION
    VIAS: TechnologyTreeVIAS
    WG: TechnologyTreeWG1
    WG_DEFAULTS: TechnologyTreeWG_DEFAULTS
    WIREWG: TechnologyTreeWIREWG

TECH: PteamLibrarySiFabTechnologyLibrary
