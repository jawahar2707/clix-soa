# Allocation Testing Guide

## Overview

The mock data has been configured to test various allocation scenarios. This guide explains the inventory setup and how to test the allocation algorithm.

## Inventory Scenarios

Based on the mock orders, inventory has been set up with 4 different scenarios:

### 1. Sufficient Stock (150% of demand)
- **Items**: A-MUFF, DZ-01/RIB/RN, IDL-01/RN/WH
- **Scenario**: These items have enough stock to fulfill all orders
- **Expected Result**: Full allocation to all customers based on priority

### 2. Limited Stock (70% of demand)
- **Items**: A-NAP, DZ-01/RIB/RNS
- **Scenario**: Stock is limited but can fulfill most orders
- **Expected Result**: Partial allocation, higher priority customers get more

### 3. Very Limited Stock (40% of demand)
- **Items**: DZ-01/RIB/CL/RN, DZ-01/RN
- **Scenario**: High competition for limited stock
- **Expected Result**: Significant partial allocation, strong prioritization

### 4. Scarce Stock (25% of demand)
- **Items**: DZ-01/RIB/CL/RNS, IDL-01/RN/CL
- **Scenario**: Maximum competition, very limited availability
- **Expected Result**: Minimal allocation, only highest priority customers

## Mock Orders

### Order #5: SIVALAYAM PRINTING AND PACKING
- **Items**: 3 items, 225 total quantity
- **Customer Profile**: Excellent payer (on-time payments)
- **Expected Priority**: High (best payment history)

### Order #6: SPICTEX COTTON MILLS PVT LTD
- **Items**: 2 items, 350 total quantity
- **Customer Profile**: Good payer
- **Expected Priority**: Medium-High

### Order #7: VIJAYVELAVAN SPINNING MILLS PVT LTD
- **Items**: 3 items, 180 total quantity
- **Customer Profile**: Average payer (some delays)
- **Expected Priority**: Medium

### Order #8: V.S TEX
- **Items**: 1 item, 300 total quantity
- **Customer Profile**: New customer (limited history)
- **Expected Priority**: Lower (limited payment history)

## Testing the Allocation

### Step 1: View Current State
1. Go to **Orders** page: http://localhost:3001/orders
2. Check that all 4 orders are in "pending" status
3. Go to **Inventory** page: http://localhost:3001/inventory
4. Verify inventory quantities match the scenarios above

### Step 2: View Customer Metrics
1. Go to **Metrics** page: http://localhost:3001/metrics
2. Review customer performance scores
3. Note the priority rankings based on:
   - Performance Score (30%)
   - Payment Frequency (25%)
   - Credit Period Adherence (25%)

### Step 3: Run Allocation
1. Go to **Allocation** page: http://localhost:3001/allocation
2. Click **"Allocate Orders"** button
3. Wait for the allocation to complete

### Step 4: Review Results
1. Check allocation results:
   - **Sufficient Stock Items**: Should show full allocation
   - **Limited Stock Items**: Should show partial allocation based on priority
   - **Scarce Stock Items**: Should show minimal allocation to top customers
2. Review allocation history table
3. Check order status updates

### Step 5: Verify Allocation Logic
The allocation should demonstrate:
- **Customer Priority**: Higher performing customers get more stock
- **Proportional Distribution**: Stock distributed based on priority scores
- **Fair Allocation**: Even lower priority customers get some allocation
- **Stock Constraints**: Respects available inventory limits

## Expected Allocation Behavior

### For Sufficient Stock Items:
- All customers should receive their full requested quantity
- No competition, all orders fulfilled

### For Limited Stock Items:
- Higher priority customers get larger share
- Lower priority customers get smaller share
- Total allocation = available stock

### For Very Limited/Scarce Stock:
- Strong prioritization based on customer metrics
- Top customers get majority of available stock
- Lower priority customers may get minimal or no allocation

## Understanding the Results

### Allocation Percentage
- **100%**: Full allocation (requested = allocated)
- **50-99%**: Partial allocation (some stock available)
- **1-49%**: Limited allocation (high competition)
- **0%**: No allocation (out of stock or lowest priority)

### Customer Priority Factors
1. **Performance Score** (30% weight)
   - Based on order history and fulfillment
2. **Payment Frequency** (25% weight)
   - Based on on-time payment percentage
3. **Credit Period Adherence** (25% weight)
   - Based on overdue payment frequency
4. **Stock Availability** (20% weight)
   - Based on available vs requested quantity

## Troubleshooting

### If allocation shows 0% for all orders:
- Check inventory quantities are set correctly
- Verify orders are in "pending" status
- Check that inventory items exist

### If all customers get equal allocation:
- Verify customer metrics are calculated
- Check payment history exists
- Review metrics calculation

### If allocation doesn't respect priority:
- Recalculate customer metrics
- Verify payment data is correct
- Check allocation algorithm weights in config

## Resetting for Testing

To reset and test again:
1. Delete mock data: `python delete_mock_data.py`
2. Recreate mock data: `python create_mock_data.py`
3. This will reset orders and inventory

## Next Steps

After testing allocation:
1. Review allocation results
2. Adjust allocation weights if needed (in `config.py`)
3. Test with different inventory scenarios
4. Export allocation results for analysis

