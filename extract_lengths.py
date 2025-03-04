import os
import csv
from paraview.simple import *
from paraview.servermanager import Fetch

# List of directories to process
directories = [
    "/media/data/Feb/copper_5um_2M",
    "/media/data/Feb/aluminum_5um_2M",
    "/media/data/Feb/iron_5um_2M",
    "/media/data/Feb/silver_5um_2M",
    "/media/data/Feb/nickel_5um_2M",
    "/media/data/Feb/titanium_5um_2M",
    "/media/data/Feb/cobalt_5um_2M"
]

# Output CSV filename
output_csv = "/media/data/Feb/all_simulations_lengths.csv"

# Dictionary to store extracted data
data_dict = {}

# Use one simulation to extract the common time steps
reference_case = "/media/data/Feb/aluminum_5um_2M/case.foam"
casefoam = OpenFOAMReader(registrationName='reference_case', FileName=reference_case)
casefoam.MeshRegions = ['internalMesh']
casefoam.CellArrays = ['alpha.metal']
casefoam.UpdatePipeline()

# Extract the time steps from the reference simulation
common_time_steps = casefoam.TimestepValues
print(f"Common time steps identified: {common_time_steps}")

# Initialize the dictionary with time values
for t in common_time_steps:
    data_dict[t] = {"Time": t}

# Process each directory
for dir_path in directories:
    material_name = os.path.basename(dir_path).replace("_", "")

    foam_file = os.path.join(dir_path, "case.foam")
    print(f"Processing: {foam_file}")

    # Create and set up the OpenFOAM reader
    casefoam = OpenFOAMReader(registrationName='case.foam', FileName=foam_file)
    casefoam.MeshRegions = ['internalMesh']
    casefoam.CellArrays = ['alpha.metal']
    casefoam.UpdatePipeline()

    # Get available time steps for this specific simulation
    timeKeeper = GetTimeKeeper()
    available_time_steps = set(casefoam.TimestepValues)

    # Set up filters
    sliceXY = Slice(registrationName='xy', Input=casefoam)
    sliceXY.SliceType = 'Plane'
    sliceXY.SliceType.Normal = [0.0, 0.0, 1.0]
    sliceXY.HyperTreeGridSlicer = 'Plane'
    sliceXY.SliceOffsetValues = [0.0]

    thresholdMetal = Threshold(registrationName='metal', Input=sliceXY)
    thresholdMetal.Scalars = ['CELLS', 'alpha.metal']
    thresholdMetal.LowerThreshold = 0.5
    thresholdMetal.UpperThreshold = 1.000000238418579

    sliceX = Slice(registrationName='x', Input=thresholdMetal)
    sliceX.SliceType = 'Plane'
    sliceX.SliceType.Normal = [0.0, 1.0, 0.0]
    sliceX.HyperTreeGridSlicer = 'Plane'
    sliceX.SliceOffsetValues = [0.0]

    sliceY = Slice(registrationName='y', Input=thresholdMetal)
    sliceY.SliceType = 'Plane'
    sliceY.SliceType.Normal = [1.0, 0.0, 0.0]
    sliceY.HyperTreeGridSlicer = 'Plane'
    sliceY.SliceOffsetValues = [0.0]

    # Process each common time step
    for t in common_time_steps:
        if t not in available_time_steps:
            # If this simulation doesn't have this time step, store "NA"
            print(f"Time step {t} missing for {material_name}, storing NA")
            data_dict[t][f"Length_x_{material_name}"] = "NA"
            data_dict[t][f"Length_y_{material_name}"] = "NA"
            continue

        print(f"Processing time step: {t} for {material_name}")

        # Set time and update pipeline
        timeKeeper.Time = t
        casefoam.UpdatePipeline(time=t)
        sliceXY.UpdatePipeline(time=t)
        thresholdMetal.UpdatePipeline(time=t)
        sliceX.UpdatePipeline(time=t)
        sliceY.UpdatePipeline(time=t)

        # Fetch data
        merged_data_x = Fetch(MergeBlocks(Input=sliceX))
        num_points_x = merged_data_x.GetNumberOfPoints()

        merged_data_y = Fetch(MergeBlocks(Input=sliceY))
        num_points_y = merged_data_y.GetNumberOfPoints()

        if num_points_x > 0 and num_points_y > 0:
            lx = merged_data_x.GetPoint(num_points_x - 1)[0] - merged_data_x.GetPoint(0)[0]
            ly = merged_data_y.GetPoint(num_points_y - 1)[1] - merged_data_y.GetPoint(0)[1]
            print(f"Time: {t}, {material_name} Length_x: {lx}, Length_y: {ly}")

            # Store data
            data_dict[t][f"Length_x_{material_name}"] = lx
            data_dict[t][f"Length_y_{material_name}"] = ly
        else:
            print(f"Time: {t}, No valid points found for {material_name}.")
            data_dict[t][f"Length_x_{material_name}"] = "NA"
            data_dict[t][f"Length_y_{material_name}"] = "NA"

# Write the final CSV file
header = ["Time"]
for dir_path in directories:
    material_name = os.path.basename(dir_path).replace("_", "")
    header.append(f"Length_x_{material_name}")
    header.append(f"Length_y_{material_name}")

with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    for t in sorted(data_dict.keys()):
        writer.writerow(data_dict[t])

print(f"Processing complete! Results saved in {output_csv}")
