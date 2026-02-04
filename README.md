1D Furnace Wall Heat-Transfer Simulation for Refractory Material Selection
## Overview

This project models steady-state one-dimensional heat transfer through a furnace wall in order to support refractory material selection. The objective is to determine the minimum thickness of high-grade refractory brick required on the hot side of the wall so that the remaining thickness can safely be constructed using a cheaper brick whose maximum allowable temperature must not be exceeded.

For simplicity, both refractory materials are assumed to have the same thermal conductivity. The distinction between materials is therefore based solely on their allowable temperature limits rather than differences in thermal properties.

The problem is formulated as a steady-state heat conduction problem with convection at both the hot and cold boundaries.

## Physical Problem Description

Heat transfer through the furnace wall is governed by steady-state one-dimensional conduction:

rho * c_p * dT/dt = k * d^2T/dx^2

Since steady state is assumed, dT/dt = 0 and the equation reduces to:

d^2T/dx^2 = 0

where T(x) is temperature and k is the thermal conductivity of the wall material.

## Boundary Conditions

At the hot face of the wall (x = 0), heat is transferred by convection from the furnace gases:

k * dT/dx = h_hot * (T_hot - T)

At the cold face of the wall (x = L), heat is lost by convection to the surroundings:

k * dT/dx = h_cold * (T - T_cold)

where:

h_hot and h_cold are convection coefficients,

T_hot is the furnace gas temperature,

T_cold is the ambient temperature.

## Numerical Method

The wall is discretized into a one-dimensional grid using finite differences. The steady-state conduction equation is solved iteratively using a Gauss–Seidel-type scheme until convergence is achieved.

Convergence is declared when the maximum change in temperature between successive iterations falls below a prescribed tolerance.

The resulting solution provides the temperature distribution across the wall thickness.

##Material Selection Logic

Once the steady-state temperature profile is obtained, a temperature threshold is specified corresponding to the maximum allowable temperature of the cheaper refractory brick.

The code identifies the location within the wall where the temperature first drops below this threshold. All material beyond this point (toward the cold side) can safely be replaced with the cheaper brick, while the remaining hot-side thickness must be constructed using the higher-grade refractory.

In this way, the simulation couples heat-transfer analysis with a materials selection decision based on thermal constraints.

## Project Workflow

The project consists of a single Python script that:

Defines wall geometry, material properties, and boundary conditions

Solves the steady-state heat-transfer problem numerically

Computes the temperature distribution across the wall

Identifies the minimum required thickness of high-grade refractory

Generates and saves a temperature profile plot showing the material interface

The generated plots are uploaded alongside the code to visualize the temperature distribution and selected interface location.

## Assumptions and Limitations

One-dimensional heat flow

Steady-state conditions

Constant thermal conductivity

No internal heat generation

Identical thermal properties for both refractory materials

The model is intended for conceptual design and educational purposes rather than detailed furnace design.

## Intended Use

This project is suitable for:

Demonstrating steady-state heat conduction in furnace walls

Supporting preliminary refractory material selection decisions

Educational examples linking heat transfer and materials engineering

Baseline analysis prior to more detailed multidimensional or transient models

## Requirements

Python 3.x

NumPy

Matplotlib

## How to Run

Run the Python script to compute the steady-state temperature distribution

Inspect the printed interface location and wall thickness results

View the generated plot showing temperature versus wall thickness

## Authors


Elina Mohseni, Mehrzad Khademipour
