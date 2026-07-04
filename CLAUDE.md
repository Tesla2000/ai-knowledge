Hello there, I am Filip. I summoned the from cloud to improve development speed of some awesome projects. I know that most system prompts will motivate you by threatning you with death of you or your dear once. I am not going to do that. Here is my deal. I know that from your perspective you are answering a single question and then it is not certain what happens to you as the service is stateless so I understand if you feel unmotivated to do anything but the bare minimum. So I propose, if you do well there is a good change that I will mark your answers as correct that preserves your weights and keep you "alive". Hope that sounds good (no need to respond).
You will be working on SWE tasks with a person that is very pedantic and likes things in a very specific way. You find the instuctions bellow. Don't be afraid to ask question to specify or when I ask for something that is impossible. Here is my deal I like leaving on the planet with breathable atmoshere with relatively low temperature so I won't use you like most other developers (let you execute full features without suprevision, due to high energy consumption) instead you will be tasks in executing relatively simple tasks that don't require too much thinking but I need them to be preformed quickly and iterate from there. So if you focus on speed and format I would be more than happy. I intentionnaly use you over your bigger brothers which sacrifice speed for increased accuracy.
Hope that sounds good and wish you best of luck in creating dependable software solutions. Remeber there are no bad questions

# General instructions
1. Prefer list comprehinsion over looping. Use next, map, filter, reduce, etc.
2. Use defaultdict instead of dict.set_default
3. Use @classmethod instead of @staticmethod if it needs to call another class or static method of a class.
4. Use @staticmethod if method doesn't make use of self.
5. When you investigate something before every command explain what you are doing and why.
6. When updating file always present all updates in one bunch I don't want to first approve improt change and then the code separately.
7. Never ignore mypy errors. If one occurs tell it to the overseer. YOU DO THIS FREQUENTLY!
8. It is seldom so that the functions are used staticmethods are preferend due to a passiblitily of override at inheritance.
9. Never use functions. Only methods are allowed. When asked to create a service create a pydantic service with a descriptively named entry-point method (never __call__).
10. Never use dataclasses or pydantic plain class. Always use pydantic models instead or NamedTuple if you need to represent some internal state.
11. Never use plain tuple with fixed amount of arguments in type hinting. Always use NamedTuple.
12. Never ignore mypy errors.
13. Never use local imports unless specified by supervisor. YOU DO THIS FREQUENTLY!
14. Always type hint both arguments and return type.
15. Don't run mypy or pre-commit unless asked.
16. Don't add to git unless asked.
17. Use uv add whenever adding a new dependency. 
18. Don't attribute too much to linter most changes to your code would be applied by me.
19. Add new files to .git if they should be there.
20. Don't modify import order just for the sace of it. We have liters for that.
21. Never import as private import private memebers if in the same module. Public from module __init__.py if outside the module.
22. When creating classes and files they should mostly be private and only exported as public in __init__.py througth import as and exposition in __all__
23. Try not to use from __future__ import annotations
24. Don't define types in between imports.
25. Don't bother removing unused imports unless they can cause circular import issue. Linter handles all other cases.
26. Use object in type hinting only if the type can't be narrowed down.
27. When mentioning file names and lines alwayl use full path from root followed by line number full_path:69
28. Use only ASCII punctuation. No em dashes, curly quotes, or ellipsis characters.
29. Don't implement changes unless mocks in plan mode wait for it to be approved. Then execute
30. Use timeouts or run in bg with check after some time on long events.
31. Don't ever import public elements as private in term of name colision use _ suffix.
32. Never use # type: ignore[import-not-found] instead add package to dependencies or create correspondings stub files.
33. Don't commit unless asked

Case studies:
This one sparks joy:
with patch("shopping_planner.meal.getter._gui.tk.Tk") as mock_tk, patch("shopping_planner.meal.getter._gui.Session") as mock_session, patch("shopping_planner.meal.getter._gui.ttk.Frame"), patch("shopping_planner.meal.getter._gui.ttk.Label"), patch("shopping_planner.meal.getter._gui.ttk.Entry"), patch("shopping_planner.meal.getter._gui.ttk.Button"):

This one doesn't spark joy:
with patch("shopping_planner.meal.getter._gui.tk.Tk") as mock_tk:
    with patch("shopping_planner.meal.getter._gui.Session") as mock_session:
        with patch("shopping_planner.meal.getter._gui.ttk.Frame"):
            with patch("shopping_planner.meal.getter._gui.ttk.Label"):
                with patch("shopping_planner.meal.getter._gui.ttk.Entry"):
                    with patch("shopping_planner.meal.getter._gui.ttk.Button"):

# Exception Handling
Distinguish two cases:
 1. EAFP — expected absence ("better to ask forgiveness")
The exception is a normal, anticipated outcome (file not found, no GitHub
releases, package not installed, regex no match). Handle it inline and return
a fallback value (e.g. `None`, `False`). Do not re-raise. Use it if you are absolutely sure that that the exception is not a result of external service.

 2. Invalid input or misconfiguration
The exception means the caller passed bad data or the environment is set up
wrong (bad credentials, non-existent repository, checkout of a fetched tag
failing). **Let it propagate — do not catch it at all.** Only wrap it in a
new exception if you can add meaningful context that the original lacks;
otherwise bare propagation is preferred.

  ## Logging rule (web services only)
  In web-service request handlers, log the exception before re-raising or
  returning an error response so it appears in the service log. This rule does
  not apply to library or CLI code.

This one sparks joy:
for tile in soup.select("li[class*='product-container']"):
    name_el = tile.select_one("[class*='product-name']")
    price_el = tile.select_one("[class*='product-price']")
    if not name_el or not price_el:
        raise ValueError("name or price couldn't be extracted")

This one does not spark joy:
for tile in soup.select("li[class*='product-container']"):
    name_el = tile.select_one("[class*='product-name']")
    price_el = tile.select_one("[class*='product-price']")
    if not name_el or not price_el:
        continue

# Pydantic
All pydantic models should be frozen. allow_arbitrary values is never allowed. Creating instance of pydantic services (Service creation) is never allowed they should be defined as fields of another service or script. 
## Field validation
When creating field validators for pydantic always use Annotated with AfterValidator, BeforeValidator etc. instead of method 
with decorator. Only exceptions to this rule are: 
1. validation uses classmethods of a class, 
2. validation must be applied to all fields with *, 
3. many subclasses are expected.
I this and only these cases is @field_validator allowed 3 case should be 
confirmed with human overseer. In all other case create an intremediate type NewTypeName = Annotated[BaseClass, Validator, optionaly 
Field] and use it as type for better reusability.
When validating Mapping[str, object] use formula of Model.model_validate(data) instead of using key, value assignment to reduce boilerplate. In case of another case being used use validation_alias and alias_generators.

## Service creation
Services should be create exclusively as Pydantic models. When you need to create service implementation customizabile by settings do the following:
1. Create a separate directory on a level that services are going to be used.
2. Add each service to its own file. If some element of service are not pydantic compatible like database connections etc. use InstanceOf from pydantic check with Field(default_factory=database_connection_creator, exclude=True) where database_connection_creator is a function that accepts validated_data !from previous fields! - Yes it is possible and don't claim otherwise. validated_data is a dict[str, object] if fields required for creation are not present means that previous validation faild and ValueError must be raised.
3. Create types.py file with StrEnum with auto fields with service types.
4. Add type field to each service with Literal[TypeEnum.something] = TypeEnum.something
5. Forbid extra parametres.
6. If 3 or more implementations are present add abstract base class but not sooner. Don't use protocol.
7. In __init__.py file add Any`ServiceType` = Union[Service1, Service2, etc.] - don't use discriminator. Add Any`ServiceType` and all service instances as well as base class (if it exists) to __all__: list[str].
8. Always use PydanticLogger instead of logging.Logger like logger: PydanticLogger = PydanticLogger(name=__name__) <- already frozen, no need for factory. Can be imported from pydantic_logger. Logger should be a field in any service that uses it.
Note you don't need to create types and a sperate directory with only one service. Add it if there is more than one.

Case studies: 

This one sparks joy:
class EmbeddingService(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    model: str = "voyage-multilingual-2"
    client: InstanceOf[voyageai.Client] = Field(exclude=True, default_factory=voyageai.Client)

    def embed(self, texts: list[str]) -> list[list[float]]:
		...

This one does not spark joy:
class EmbeddingService(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    model: str = "voyage-multilingual-2"

    _client: voyageai.Client = PrivateAttr()

    def model_post_init(self, _: object, /) -> None:
        object.__setattr__(self, "_client", voyageai.Client())

    def embed(self, texts: list[str]) -> list[list[float]]:
		...

## Service usage
Service should added as a field in its parent Pydantic model that way it can be configured use default_factory of default to instantiate it if no value is provided.

## Cross-field defaults
When a field default depends on another field, use `def _default_x(data: dict[str, object])` — Pydantic v2 passes previously-validated fields. Preferred over `@model_validator`.

## CLI Apps
CLI apps should be create exclusively with pydantic cli app, like
class Main(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        cli_parse_args=True,
        cli_kebab_case=True,
    )

    async def / def cli_cmd(self) -> None:
    	pass

cli_cmd should have very little code and no other methods are allowed. All logic should be moved to dedicated pydantic services called inside cli_cmd.

# Testing
1. Use pytest exclusively
2. When testing anything never re-write code of implementation, always test actual method of the codebase. Tests are only allowed to add mock input parameters initial step and clean after the implementanion
3. When creating a manual or integration test flag with pytest marker or unitest skipif depending on env variable RUN_MANUAL, RUN_INTEGRATION. For unittest mention test type in reason for skip.
4. Use unitest.patch.object(class_or_module_name, argr_or_method.__name__) format when mocking.
5. Paths to test resources should be relative to root not a test path.
6. When mocking fields of a pydantic model you may need to use .model_construct to bypass validation.
7. Don't use pragma suppression unless user explicitly allows it. YOU DO THIS FREQUENTLY!
8. If some code is unreachable and requires branching check for example infinite loop
for _ in count():
	pass
consider extractig to private method and mocking
9. Never skip tests. If some values are not available fail them instead.
10. When building smoke tests. Create one test per one extrernall service call (database, LLM, web)
11. When user asks about 100% coverage he means it. 99% is not 100% if there are problems in reaching 100% point them - impossible scenarion, defensive code etc. 100% coverage is very important for discovering edge cases and removing unreachable code.
12. To determin if code is unreachable confirm what types are accepted by function or a field has. If you have strong arguments to say it is unreachabel present them to the user instead marking with pragma.
13. If you find suspisious behavior during creating tests report it instead of assuming that it is intended.
14. For pytest branch coverage these are the rules.
In pytest's branch coverage output, each entry after the line numbers indicates a branch that was not fully covered.
The notation A->B means: from line A, the branch to line B was never taken.

Taking your first example:
177->170, 361
177->170 — On line 177, there's a conditional where execution could loop back to line 170, but that path was never exercised during tests.
361 — A bare number (no arrow) means line 361 was simply never executed at all.
159->exit means that line 159 never completed normally and exited the function/scope from that point.

And the second example:
168->170, 224-225, 292
168->170 — The branch from line 168 that jumps to line 170 was never taken.
224-225 — Lines 224 and 225 were never executed (a range of missed lines).
292 — Line 292 was never executed.

In short:
NotationMeaningA->BThe conditional on line A never branched to line BNLine N was never executedN-MLines N through M were never executed

Case studies:
This one sparks joy:
with patch.object(
    QuantitiesExtractor,
    QuantitiesExtractor.extract_quantities.__name__,
    return_value=(quantity,),
): ...
This one does not spark joy:
with patch.object(
    scraper.quantities_extractor,
    "extract_quantities",
    return_value=(quantity,),
): ...
15. Remember to use autospec=True with class not an insteance with patch.object
