// Fill out your copyright notice in the Description page of Project Settings.

#include "AsteroidPickUp.h"

#include "Components/StaticMeshComponent.h"

AAsteroidPickUp::AAsteroidPickUp()
{
	PickUpMeshComponent->SetSimulatePhysics(true);
}
