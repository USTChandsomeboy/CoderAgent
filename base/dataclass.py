from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any


@dataclass.dataclass
class LearningPath(dataclass.DataClass):

    name: str
    description: str
    courses: List[str]


import json
from dataclasses import dataclass, asdict, is_dataclass, fields
from typing import Type, TypeVar, List, Any, get_origin, get_args, Union

# 泛型类型，用于类型检查
T = TypeVar("T")

@dataclass
class BaseDataClass:
    @classmethod
    def from_dict(cls: Type[T], data: Any) -> T:
        """
        从字典或列表转换为 dataclass 实例，支持嵌套 dataclass 和列表。
        """
        if isinstance(data, list):
            return [cls.from_dict(item) if isinstance(item, dict) else item for item in data]

        if not isinstance(data, dict):
            raise TypeError("Input data must be a dictionary or list")

        field_values = {}
        for field in fields(cls):
            field_type = field.type
            field_value = data.get(field.name)

            # 检查字段类型是否为 dataclass 类型（嵌套支持）
            if is_dataclass(field_type):
                field_values[field.name] = field_type.from_dict(field_value)
            elif get_origin(field_type) == list:  # 检查是否为 List 类型
                inner_type = get_args(field_type)[0]
                if is_dataclass(inner_type):
                    field_values[field.name] = [inner_type.from_dict(item) for item in field_value]
                else:
                    field_values[field.name] = field_value
            else:
                field_values[field.name] = field_value

        return cls(**field_values)

    def to_dict(self) -> Any:
        """
        将 dataclass 实例转换为字典或列表，支持嵌套 dataclass 和列表。
        """
        return asdict(self)

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> Union[T, List[T]]:
        """
        从 JSON 字符串转换为 dataclass 实例或列表。
        """
        data = json.loads(json_str)
        if isinstance(data, list):
            return [cls.from_dict(item) if isinstance(item, dict) else item for item in data]
        return cls.from_dict(data)

    def to_json(self) -> str:
        """
        将 dataclass 实例转换为 JSON 字符串。
        """
        return json.dumps(self.to_dict(), indent=4)