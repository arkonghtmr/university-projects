// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AsteroidSpawner.generated.h"

class APickUpBase;
class UBoxComponent;

UCLASS()
class UNREALDEVELOPMENT_API AAsteroidSpawner : public AActor
{
	GENERATED_BODY()

public:
	AAsteroidSpawner();

protected:
	virtual void BeginPlay() override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawner")
	UBoxComponent* SpawnBoxComponent;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawner")
	TSubclassOf<APickUpBase> ActorToSpawn;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawner")
	float MinSpawnDelay;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Spawner")
	float MaxSpawnDelay;

	FVector GetRandomSpawnPoint() const;

private:
	void SpawnActors();
	void StartSpawnTimer();

	FTimerHandle SpawnTimerHandle;
	float RandomSpawnDelay;
};
