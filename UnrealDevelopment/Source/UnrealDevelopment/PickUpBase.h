#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "PickUpBase.generated.h"

UCLASS()
class YOURPROJECT_API APickUpBase : public AActor
{
	GENERATED_BODY()
    
public:    
	APickUpBase();

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	// Компонент меша с макросом UPROPERTY
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mesh")
	UStaticMeshComponent* PickUpMeshComponent;

	// Булево поле активности
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Status")
	bool bIsActive;

public:
	// Методы для Blueprint
	UFUNCTION(BlueprintPure, Category = "Status")
	bool GetIsActive() const;

	UFUNCTION(BlueprintCallable, Category = "Status")
	void SetIsActive(bool NewValue);
};