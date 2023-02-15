from products.models import Basket


def baskets(request) -> dict['baskets': Basket]:
    """Данный контекстный процессор позволяет пользоваться переменной baskets
    глобально; подключается в настройках в переменной TEMPLATES
    """

    user = request.user
    return {'baskets': Basket.objects.filter(
        user=user) if user.is_authenticated else []}
