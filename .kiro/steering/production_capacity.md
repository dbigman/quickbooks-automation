# Production Line Capacity & Staffing

## Overview

This document defines the statistical capacity calculations and staffing requirements for each production line. Capacity is calculated based on historical performance data, equipment specifications, and operator efficiency metrics.

## Production Line Capacity (Statistical Analysis)

### Methodology
Capacity calculations are based on:
- **Historical throughput data**: 6-month rolling average
- **Equipment cycle times**: Measured bottleneck analysis
- **Operator efficiency**: Skill level and experience factors
- **Quality factors**: Rework and rejection rates
- **Maintenance downtime**: Planned and unplanned downtime statistics

### Line Capacity & Staffing Matrix

| Line Code | Line Name | Operators Required | Base Capacity (units/hour) | Peak Capacity (units/hour) | Efficiency Factor |
|-----------|-----------|-------------------|---------------------------|---------------------------|------------------|
| `a_det_galon` | Detergent Gallon Line | 3 | 500 | 800 | 0.85 |
| `g_alimentos_galon` | Food Gallon Line | 3 | 450 | 750 | 0.82 |
| `b_det_32oz` | Detergent 32oz Line | 3 | 1,200 | 1,800 | 0.88 |
| `h_alimentos_16oz` | Food 16oz Line | 3 | 1,500 | 2,200 | 0.90 |
| `d_det_pailas` | Detergent 5-Gallon Line | 2 | 200 | 400 | 0.75 |
| `i_alimentos_polvo` | Food Powder Line | 5 | 600 | 1,000 | 0.80 |
| `e_det_piston` | Detergent Piston/Pump Line | 1 | 800 | 1,200 | 0.92 |
| `j_alimentos_manual` | Food Manual/Solid Line | 1 | 100 | 300 | 0.65 |
| `k_alimentos_liquido_manual` | Food Liquid Manual Line | 1 | 150 | 250 | 0.70 |
| `f_det_manual` | Detergent Manual/Bulk Line | 1 | 50 | 150 | 0.60 |
| `z_sudoc` | SUDOC Specialty Line | 1 | 75 | 200 | 0.68 |

## Operator Role Definitions

### 3-Operator Lines (A, G, B, H)
**High-volume automated lines requiring coordinated team operation**

**Operator 1 - Line Lead/Quality Controller**:
- Overall line supervision and quality monitoring
- Equipment troubleshooting and minor adjustments
- Batch documentation and lot tracking
- Communication with production planning

**Operator 2 - Material Handler/Feeder**:
- Raw material preparation and feeding
- Container supply and changeover assistance
- Finished goods handling and staging
- Inventory tracking and replenishment

**Operator 3 - Packaging/Case Packer**:
- Final packaging and case formation
- Label application verification
- End-of-line quality checks
- Palletizing and shipping preparation

### 2-Operator Lines (D)
**Medium-volume lines with heavy container handling**

**Operator 1 - Line Operator/Quality**:
- Primary line operation and monitoring
- Quality control and batch documentation
- Equipment maintenance coordination

**Operator 2 - Material Handler**:
- Heavy container handling (5-gallon)
- Material preparation and feeding
- Finished goods staging and palletizing

### 5-Operator Lines (I)
**Complex powder handling requiring specialized skills**

**Operator 1 - Line Lead/Powder Specialist**:
- Powder system operation and monitoring
- Dust control system management
- Quality control and testing
- Batch formulation verification

**Operator 2 - Filling Operator**:
- Powder filling system operation
- Weight verification and adjustment
- Container feeding and positioning

**Operator 3 - Packaging Operator**:
- Container sealing and capping
- Label application and verification
- Case packing and coding

**Operator 4 - Material Handler**:
- Raw material preparation and blending
- Ingredient staging and feeding
- Finished goods handling

**Operator 5 - Utility/Cleaner**:
- Line cleaning and sanitization
- Dust collection maintenance
- Equipment cleaning between batches
- Safety and housekeeping

### 1-Operator Lines (E, J, K, F, Z)
**Semi-automated or manual lines with single operator control**

**Operator 1 - Multi-skilled Operator**:
- Complete line operation and monitoring
- Quality control and documentation
- Material handling and preparation
- Basic maintenance and troubleshooting
- Packaging and finishing operations

## Capacity Calculation Formulas

### Theoretical Capacity
```
Theoretical Capacity = Equipment Cycle Rate × Operating Hours × Availability Factor
```

### Effective Capacity
```
Effective Capacity = Theoretical Capacity × Efficiency Factor × Quality Factor
```

### Labor-Adjusted Capacity
```
Labor-Adjusted Capacity = Effective Capacity × Operator Skill Factor × Staffing Level Factor
```

## Capacity Constraints & Bottlenecks

### Equipment Bottlenecks
- **Filling Systems**: Primary constraint on liquid lines
- **Capping Systems**: Secondary constraint on high-speed lines
- **Powder Handling**: Primary constraint on powder lines
- **Manual Operations**: Primary constraint on manual lines

### Labor Constraints
- **Skill Requirements**: Specialized skills for powder and food lines
- **Training Time**: 2-4 weeks for new operators on complex lines
- **Shift Coverage**: 24/7 operation requires 4.2 FTE per position
- **Cross-training**: 20% capacity reduction during training periods

### Quality Constraints
- **Food Safety**: Additional quality checks reduce effective capacity by 5-10%
- **Regulatory Compliance**: Documentation requirements impact throughput
- **Customer Specifications**: Special requirements may reduce line efficiency

## Shift Patterns & Staffing

### Standard Shift Pattern
- **Day Shift**: 6:00 AM - 2:00 PM
- **Evening Shift**: 2:00 PM - 10:00 PM  
- **Night Shift**: 10:00 PM - 6:00 AM

### Staffing Multipliers
- **Single Shift Operation**: 1.0 × Base Staffing
- **Two Shift Operation**: 2.2 × Base Staffing (10% overlap)
- **Three Shift Operation**: 3.5 × Base Staffing (coverage + relief)
- **24/7 Operation**: 4.2 × Base Staffing (full coverage + vacation/sick)

## Performance Metrics & KPIs

### Capacity Utilization
- **Target Utilization**: 85% of effective capacity
- **Peak Utilization**: 95% of effective capacity (short periods)
- **Minimum Utilization**: 60% (below this, consider line shutdown)

### Efficiency Metrics
- **Overall Equipment Effectiveness (OEE)**: Target 85%
- **Labor Efficiency**: Actual vs. standard labor hours
- **Quality Efficiency**: First-pass yield percentage
- **Schedule Adherence**: On-time completion percentage

### Capacity Planning Factors

#### Seasonal Adjustments
- **Q4 Holiday Season**: +15% capacity demand
- **Q1 Post-Holiday**: -10% capacity demand
- **Summer Months**: +5% for cleaning products
- **Back-to-School**: +8% for food products

#### Product Mix Impact
- **High-Volume Products**: +10% efficiency due to longer runs
- **Specialty Products**: -15% efficiency due to changeovers
- **New Product Introduction**: -20% efficiency during ramp-up
- **Quality Issues**: -25% efficiency during problem resolution

## Integration with MPS System

### Capacity Data Structure
```python
PRODUCTION_CAPACITY = {
    'a_det_galon': {
        'operators_required': 3,
        'base_capacity_per_hour': 500,
        'peak_capacity_per_hour': 800,
        'efficiency_factor': 0.85,
        'bottleneck': 'liquid_filler_1',
        'shift_multiplier': 1.0  # Single shift base
    },
    'i_alimentos_polvo': {
        'operators_required': 5,
        'base_capacity_per_hour': 600,
        'peak_capacity_per_hour': 1000,
        'efficiency_factor': 0.80,
        'bottleneck': 'powder_filler',
        'shift_multiplier': 1.0
    }
    # ... additional lines
}
```

### Capacity Planning Functions
- **Real-time capacity calculation** based on current staffing
- **Constraint-based scheduling** considering bottlenecks
- **Labor cost optimization** in production planning
- **Capacity vs. demand analysis** for resource allocation

## Continuous Improvement

### Capacity Enhancement Initiatives
- **Operator training programs**: Target 5% efficiency improvement annually
- **Equipment upgrades**: Bottleneck elimination projects
- **Process optimization**: Lean manufacturing implementation
- **Automation projects**: Reduce labor dependency on manual lines

### Data Collection & Analysis
- **Real-time production data**: Integration with line control systems
- **Labor tracking**: Actual vs. planned labor hours
- **Quality metrics**: Impact on effective capacity
- **Maintenance data**: Downtime impact on capacity

This capacity document provides the statistical foundation for accurate production planning and resource allocation within the MPS system.