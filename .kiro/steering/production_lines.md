# Production Lines & Production Vessels

## Overview

This document defines the production line structure and machinery configuration for the manufacturing facility. The system tracks production across multiple specialized lines, each equipped with specific machinery for different product types and container sizes.

## Production Line Structure

Based on the product categorization data, the facility operates **12 distinct production lines**, each optimized for specific product categories and container types:

### Detergent Production Lines

#### Line A - Detergent Gallon Production (`a_det_galon`)

**Primary Products**: 4/1 gallon detergent products (multipurpose cleaners, degreasers, dishwash, disinfectants, alcohol-based products)

**Machinery Configuration**:

1. **liquid_filler_1**: High-capacity gallon filling station with precision flow control
2. **capper_1**: Automatic cap application and torque system for gallon containers
3. **labeler_1**: Wrap-around labeling system for gallon jugs
4. **conveyor_1**: Heavy-duty conveyor system for gallon containers
5. **quality_control_station**: Automated weight and seal verification

#### Line B - Detergent 32oz Production (`b_det_32oz`)

**Primary Products**: 12/32oz and 24/16oz detergent products (alcohol, bath & tile cleaners, multipurpose cleaners)

**Machinery Configuration**:

1. **liquid_filler_2**: Multi-head filling system for 32oz containers
2. **capper_2**: Trigger sprayer and cap application system
3. **labeler_2**: Front and back labeling system
4. **conveyor_2**: Standard conveyor for smaller containers
5. **case_packer**: Automated case packing for 12-count cases

#### Line D - Detergent 5-Gallon Production (`d_det_pailas`)

**Primary Products**: 5-gallon industrial detergent products (heavy-duty cleaners, laundry chemicals)

**Machinery Configuration**:

1. **liquid_filler_3**: Large-volume filling system for 5-gallon containers
2. **capper_3**: Heavy-duty capping system for 5-gallon lids
3. **labeler_3**: Large format labeling system
4. **conveyor_3**: Reinforced conveyor for heavy containers
5. **handle_applicator**: Automatic handle attachment system

#### Line E - Detergent Piston/Pump Production (`e_det_piston`)

**Primary Products**: Pump and piston-dispensed products (hand soaps, sanitizers, body wash)

**Machinery Configuration**:

1. **liquid_filler_4**: Precision piston filling system
2. **pump_applicator**: Automatic pump mechanism installation
3. **labeler_4**: Cylindrical container labeling system
4. **conveyor_4**: Gentle handling conveyor for pump containers
5. **quality_tester**: Pump mechanism functionality testing

#### Line F - Detergent Manual/Bulk Production (`f_det_manual`)

**Primary Products**: Large volume and specialty chemical products (55-gallon drums, 260-gallon totes)

**Machinery Configuration**:

1. **bulk_filler**: High-volume drum and tote filling system
2. **drum_capper**: Heavy-duty drum lid sealing system
3. **drum_labeler**: Large format drum labeling system
4. **forklift_station**: Material handling equipment integration
5. **hazmat_sealer**: Specialized sealing for hazardous materials

### Food Production Lines

#### Line G - Food Gallon Production (`g_alimentos_galon`)

**Primary Products**: 4/1 gallon food products (adobo, soy sauce, vanilla, vinegar)

**Machinery Configuration**:

1. **liquid_filler_5**: Food-grade gallon filling system with CIP capability
2. **capper_5**: Food-grade capping system with tamper-evident seals
3. **labeler_5**: Food-grade labeling with nutritional information capability
4. **conveyor_5**: Stainless steel food-grade conveyor
5. **date_coder**: Automated date/lot coding system

#### Line H - Food 16oz Production (`h_alimentos_16oz`)

**Primary Products**: 24/16oz food products (soy sauce, vanilla, vinegar)

**Machinery Configuration**:

1. **liquid_filler_6**: Multi-head food-grade filling for 16oz bottles
2. **capper_6**: Screw cap application for food bottles
3. **labeler_6**: Front and back food labeling system
4. **conveyor_6**: Food-grade conveyor with gentle handling
5. **case_packer_2**: Food-grade case packing for 24-count cases

#### Line I - Food Powder Production (`i_alimentos_polvo`)

**Primary Products**: Powdered food products (adobo, sazon, spices in various sizes)

**Machinery Configuration**:

1. **powder_filler**: Auger-based powder filling system with dust control
2. **container_feeder**: Automatic container feeding system
3. **capper_7**: Powder-specific capping system with liner insertion
4. **labeler_7**: Powder container labeling system
5. **dust_collection**: Industrial dust collection and filtration system

#### Line J - Food Manual/Solid Production (`j_alimentos_manual` / `j_alimentos_solido_manual`)

**Primary Products**: Manual packaging of solid food products (spices, seasonings, specialty items)

**Machinery Configuration**:

1. **manual_fill_station**: Ergonomic manual filling stations
2. **scale_system**: Precision weighing and portioning scales
3. **sealer**: Heat sealing system for flexible packaging
4. **labeler_8**: Manual/semi-automatic labeling system
5. **packaging_station**: Final packaging and quality control station

#### Line K - Food Liquid Manual Production (`k_alimentos_liquido_manual`)

**Primary Products**: Specialty liquid food products (food coloring, flavorings, large volume vanilla)

**Machinery Configuration**:

1. **precision_filler**: Small-volume precision filling system
2. **dropper_applicator**: Dropper cap application system
3. **labeler_9**: Small container labeling system
4. **conveyor_7**: Precision handling conveyor
5. **quality_station**: Color and consistency verification

### Specialty Production Lines

#### Line Z - SUDOC Production (`z_sudoc`)

**Primary Products**: Specialized cleaning and restoration products

**Machinery Configuration**:

1. **specialty_filler**: Multi-product filling system for various container types
2. **capper_8**: Universal capping system for diverse container types
3. **labeler_10**: Variable format labeling system
4. **conveyor_8**: Flexible conveyor system
5. **packaging_system**: Custom packaging for specialty products

## Production Capacity & Scheduling

### Line Capacity Reference

Production line capacities, operator requirements, and statistical performance data are maintained in the separate **Production Capacity Document** (`production_capacity.md`). This includes:

- Statistical capacity calculations based on historical data
- Operator staffing requirements per line
- Efficiency factors and bottleneck analysis
- Labor-adjusted capacity formulas
- Shift patterns and staffing multipliers

**Key Capacity Summary**:

- **High-Volume Lines**: 1,200-2,200 units/hour (B, H)
- **Medium-Volume Lines**: 450-1,000 units/hour (A, G, I, E)
- **Low-Volume Lines**: 50-400 units/hour (D, F, J, K, Z)
- **Operator Requirements**: 1-5 operators per line depending on complexity

### Production Scheduling Rules

1. **Food Safety Priority**: Food lines (G, H, I, J, K) have priority scheduling for freshness
2. **Changeover Time**: Allow 2-4 hours for major product changeovers
3. **CIP Cycles**: Food lines require daily Clean-in-Place cycles
4. **Batch Tracking**: All production requires lot number tracking
5. **Quality Holds**: 24-hour quality hold for new product runs

## Maintenance & Cleaning Protocols

### Daily Maintenance

- **Pre-shift inspection**: All machinery safety and operational checks
- **Lubrication**: Automated lubrication systems on high-speed lines
- **Calibration**: Daily calibration of filling systems and scales
- **Cleaning**: End-of-shift cleaning protocols (enhanced for food lines)

### Weekly Maintenance

- **Deep cleaning**: Complete line sanitization
- **Preventive maintenance**: Scheduled component replacement
- **Calibration verification**: Third-party calibration verification
- **Safety system testing**: Emergency stop and safety interlock testing

### Monthly Maintenance

- **Major component inspection**: Bearings, motors, drive systems
- **Electrical system testing**: Control panel and sensor verification
- **Mechanical alignment**: Conveyor and machinery alignment checks
- **Performance optimization**: Speed and efficiency optimization

## Quality Control Integration

### In-Line Quality Systems

- **Fill weight verification**: Automatic weight checking on all lines
- **Cap torque testing**: Automated torque verification
- **Label placement verification**: Vision systems for label alignment
- **Leak testing**: Pressure testing for sealed containers
- **Date code verification**: Automatic date code reading and verification

### Laboratory Integration

- **Sample collection**: Automated sample collection from each line
- **Batch release**: Electronic batch release system integration
- **Traceability**: Complete ingredient to finished product traceability
- **Recall capability**: Rapid product recall identification system

## Environmental & Safety Systems

### Environmental Controls

- **Dust collection**: Industrial dust collection on powder lines
- **Vapor control**: Solvent vapor capture and treatment
- **Wastewater treatment**: Process water treatment and recycling
- **Energy monitoring**: Real-time energy consumption tracking

### Safety Systems

- **Emergency stops**: Accessible emergency stops throughout each line
- **Safety interlocks**: Automatic safety shutdown systems
- **Personal protective equipment**: Line-specific PPE requirements
- **Hazardous material handling**: Specialized handling for chemical products

## Integration with MPS System

### Production Planning

- **Line capacity constraints**: Real-time capacity planning integration
- **Changeover optimization**: Minimize changeover time in scheduling
- **Material requirements**: Automatic BOM-based material planning
- **Quality scheduling**: Integration with quality testing schedules

### Performance Monitoring

- **OEE tracking**: Overall Equipment Effectiveness monitoring
- **Downtime analysis**: Automatic downtime categorization and reporting
- **Efficiency optimization**: Continuous improvement data collection
- **Predictive maintenance**: Equipment health monitoring and prediction

## Implementation Notes

### Code Integration

When implementing production line logic in the MPS system:

1. **Use production_line field**: Reference the exact production line codes (a_det_galon, b_det_32oz, etc.)
2. **Capacity constraints**: Apply line-specific capacity limits in scheduling algorithms
3. **Changeover costs**: Include changeover time and costs in optimization calculations
4. **Quality requirements**: Factor in quality hold times and testing requirements
5. **Maintenance windows**: Schedule around planned maintenance windows

### Data Structure

```python
PRODUCTION_LINES = {
    'a_det_galon': {
        'name': 'Detergent Gallon Line',
        'changeover_time_hours': 3,
        'machinery': ['liquid_filler_1', 'capper_1', 'labeler_1', 'conveyor_1', 'quality_control_station'],
        'food_grade': False,
        'cip_required': False
    },
    'g_alimentos_galon': {
        'name': 'Food Gallon Line',
        'changeover_time_hours': 4,  # Longer due to food safety requirements
        'machinery': ['liquid_filler_5', 'capper_5', 'labeler_5', 'conveyor_5', 'date_coder'],
        'food_grade': True,
        'cip_required': True
    }
    # ... additional lines
}

# Capacity data is maintained separately in production_capacity.md
# Import capacity data: from production_capacity import PRODUCTION_CAPACITY
```

This production line configuration provides the foundation for accurate production planning, capacity management, and manufacturing execution within the MPS system.
