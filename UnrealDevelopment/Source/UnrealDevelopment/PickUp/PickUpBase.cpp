// Fill out your copyright notice in the Description page of Project Settings.

#include "PickUpBase.h"

#include "Components/StaticMeshComponent.h"

APickUpBase::APickUpBase()
{
	PrimaryActorTick.bCanEverTick = true;

	PickUpMeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Pick Up Mesh"));
	RootComponent = PickUpMeshComponent;

	bIsActive = true;
}

void APickUpBase::BeginPlay()
{
	Super::BeginPlay();
}

void APickUpBase::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
}

bool APickUpBase::GetIsActive() const
{
	return bIsActive;
}

void APickUpBase::SetIsActive(bool NewIsActive)
{
	bIsActive = NewIsActive;
}
