// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PickUpBase.generated.h"

class UStaticMeshComponent;

UCLASS()
class UNREALDEVELOPMENT_API APickUpBase : public AActor
{
	GENERATED_BODY()

public:
	APickUpBase();

protected:
	virtual void BeginPlay() override;

public:
	virtual void Tick(float DeltaTime) override;

protected:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Mesh")
	UStaticMeshComponent* PickUpMeshComponent;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PickUp")
	bool bIsActive;

public:
	UFUNCTION(BlueprintPure, Category = "PickUp")
	bool GetIsActive() const;

	UFUNCTION(BlueprintCallable, Category = "PickUp")
	void SetIsActive(bool NewIsActive);
};
