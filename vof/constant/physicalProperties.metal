/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  10
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    location    "constant";
    object      physicalProperties.water;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
viscosityModel  constant;

nu          5.4641e-07; // Copper kinematic viscosity [m^2/s]
rho         8022.22; // Copper density [Kg/m^3]

Tsolidus    1355.0; // Copper [K] specified by Me
Tliquidus   1356.0; // Copper [K]

LatentHeat 6.2e6;   // unspecified
beta       5.0e-6;  // unspecified

poly_kappa   (25 0.0 0 0 0 0 0 0);  // unspecified
poly_cp   (700 0.0 0 0 0 0 0 0);    // unspecified
// ************************************************************************* //
