// Fill out your copyright notice in the Description page of Project Settings.

#include "AsteroidSpawner.h"

#include "Components/BoxComponent.h"
#include "Kismet/KismetMathLibrary.h"
#include "../PickUp/PickUpBase.h"
#include "TimerManager.h"

AAsteroidSpawner::AAsteroidSpawner()
{
	PrimaryActorTick.bCanEverTick = false;

	SpawnBoxComponent = CreateDefaultSubobject<UBoxComponent>(TEXT("Spawn Box"));
	RootComponent = SpawnBoxComponent;

	MinSpawnDelay = 1.0f;
	MaxSpawnDelay = 3.0f;
	RandomSpawnDelay = 0.0f;
}

void AAsteroidSpawner::BeginPlay()
{
	Super::BeginPlay();

	StartSpawnTimer();
}

FVector AAsteroidSpawner::GetRandomSpawnPoint() const
{
	if (!SpawnBoxComponent)
	{
		return GetActorLocation();
	}

	const FVector Origin = SpawnBoxComponent->GetComponentLocation();
	const FVector BoxExtent = SpawnBoxComponent->GetScaledBoxExtent();

	return UKismetMathLibrary::RandomPointInBoundingBox(Origin, BoxExtent);
}

void AAsteroidSpawner::SpawnActors()
{
	if (!ActorToSpawn || !GetWorld())
	{
		StartSpawnTimer();
		return;
	}

	FActorSpawnParameters Parameters;
	Parameters.Owner = this;
	Parameters.Instigator = GetInstigator();
	Parameters.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;

	APickUpBase* SpawnedActor = GetWorld()->SpawnActor<APickUpBase>(
		ActorToSpawn,
		GetRandomSpawnPoint(),
		UKismetMathLibrary::RandomRotator(),
		Parameters
	);

	StartSpawnTimer();
}

void AAsteroidSpawner::StartSpawnTimer()
{
	if (!GetWorld())
	{
		return;
	}

	RandomSpawnDelay = UKismetMathLibrary::RandomFloatInRange(MinSpawnDelay, MaxSpawnDelay);

	GetWorld()->GetTimerManager().SetTimer(
		SpawnTimerHandle,
		this,
		&AAsteroidSpawner::SpawnActors,
		RandomSpawnDelay,
		false
	);
}
