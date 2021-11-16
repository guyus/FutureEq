@echo off
PowerShell.exe -Command "& {Start-Process PowerShell.exe 'pause Enable-NetAdapterBinding -ComponentID jnprns -InterfaceDescription "Juniper Networks Virtual Adapter"' -Verb RunAs}"
