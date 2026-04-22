#include "PickUpBase.h"

APickUpBase::APickUpBase()
{
	// Создание компонента меша
	PickUpMeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Pick Up Mesh"));
	RootComponent = PickUpMeshComponent; // Установка как корневого компонента
    
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

// Реализация методов
bool APickUpBase::GetIsActive() const
{
	return bIsActive;
}

void APickUpBase::SetIsActive(bool NewValue)
{
	bIsActive = NewValue;
}