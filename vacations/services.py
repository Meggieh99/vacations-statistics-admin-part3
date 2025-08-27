from typing import Optional
from django.core.exceptions import ValidationError
from datetime import date
from typing import List
from vacations.models import User, Vacation,Country,Like, Role


def register_user(first_name: str, last_name: str, email: str, password: str) -> User:
    """
    Create and return a new user after validating input.
    
    :param first_name: First name of the user
    :param last_name: Last name of the user
    :param email: Email address (must be unique)
    :param password: Password (must be at least 4 characters)
    :raises ValidationError: If email exists or password is too short
    :return: Created User instance
    """
    if len(password) < 4:
        raise ValidationError("Password must be at least 4 characters long.")
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already exists.")
    user_role = Role.objects.get(name='user')
    return User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role=user_role
    )


def login_user(email: str, password: str) -> Optional[User]:
    """
    Return a user if email and password match; otherwise None.

    :param email: User's email
    :param password: User's password
    :return: User object or None
    """
    return User.objects.filter(email=email, password=password).first()


def add_like(user_id: int, vacation_id: int) -> Like:
    """
    Add a like to a vacation by a user.

    :param user_id: ID of the user
    :param vacation_id: ID of the vacation
    :raises ValidationError: If like already exists
    :return: Created Like instance
    """
    if Like.objects.filter(user_id=user_id, vacation_id=vacation_id).exists():
        raise ValidationError("Like already exists.")
    return Like.objects.create(user_id=user_id, vacation_id=vacation_id)


def remove_like(user_id: int, vacation_id: int) -> None:
    """
    Remove a like from a vacation by a user.

    :param user_id: ID of the user
    :param vacation_id: ID of the vacation
    """
    Like.objects.filter(user_id=user_id, vacation_id=vacation_id).delete()

    
def add_vacation(
    country_id: int, description: str, start_date: date, end_date: date, price: float, image_filename: str
) -> Vacation:
    """
    Add a new vacation after validating business rules.

    :param country_id: ID of the country
    :param description: Vacation description
    :param start_date: Vacation start date
    :param end_date: Vacation end date
    :param price: Vacation price
    :param image_filename: Image file name
    :raises ValidationError: If business rules are violated
    :return: Created Vacation instance
    """
    if price < 0 or price > 10000:
        raise ValidationError("Price must be between 0 and 10,000.")
    if end_date < start_date:
        raise ValidationError("End date cannot be before start date.")
    if start_date < date.today():
        raise ValidationError("Start date cannot be in the past.")
    
    country = Country.objects.get(id=country_id)
    return Vacation.objects.create(
        country=country,
        description=description,
        start_date=start_date,
        end_date=end_date,
        price=price,
        image_filename=image_filename
    )

def update_vacation(
    vacation_id: int, description: str, start_date: date, end_date: date, price: float, image_filename: str = ""
) -> Vacation:
    """
    Update an existing vacation after validating business rules.

    :param vacation_id: ID of the vacation to update
    :param description: New description
    :param start_date: New start date
    :param end_date: New end date
    :param price: New price
    :param image_filename: Optional new image file name
    :raises ValidationError: If business rules are violated
    :return: Updated Vacation instance
    """
    if price < 0 or price > 10000:
        raise ValidationError("Price must be between 0 and 10,000.")
    if end_date < start_date:
        raise ValidationError("End date cannot be before start date.")
    
    vacation = Vacation.objects.get(id=vacation_id)
    vacation.description = description
    vacation.start_date = start_date
    vacation.end_date = end_date
    vacation.price = price
    if image_filename:
        vacation.image_filename = image_filename
    vacation.save()
    return vacation

def delete_vacation(vacation_id: int) -> None:
    """
    Delete a vacation and its related likes.

    :param vacation_id: ID of the vacation to delete
    """
    Vacation.objects.filter(id=vacation_id).delete()

def get_all_vacations() -> List[Vacation]:
    """
    Retrieve all vacations ordered by start date ascending.

    :return: List of Vacation objects
    """
    return list(Vacation.objects.all().order_by('start_date'))

def add_country(name: str) -> Country:
    """
    Add a new country if it does not already exist.

    :param name: Name of the country
    :raises ValidationError: If the country already exists
    :return: Created Country instance
    """
    if Country.objects.filter(name=name).exists():
        raise ValidationError("Country with this name already exists.")
    return Country.objects.create(name=name)

def get_all_countries() -> List[Country]:
    """
    Retrieve all countries.

    :return: List of Country objects
    """
    return list(Country.objects.all())

def delete_country(country_id: int) -> None:
    """
    Delete a country by ID.

    :param country_id: ID of the country to delete
    """
    Country.objects.filter(id=country_id).delete()

def add_role(name: str) -> Role:
    """
    Add a new role if it does not already exist.

    :param name: Name of the role
    :raises ValidationError: If the role already exists
    :return: Created Role instance
    """
    if Role.objects.filter(name=name).exists():
        raise ValidationError("Role with this name already exists.")
    return Role.objects.create(name=name)

def get_all_roles() -> List[Role]:
    """
    Retrieve all roles.

    :return: List of Role objects
    """
    return list(Role.objects.all())



