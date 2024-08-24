from pydantic import BaseModel, Field, field_validator


class JWTToken(BaseModel):
    exp: int
    iat: int
    auth_time: int
    jti: str
    iss: str
    aud: str
    sub: str
    typ: str
    azp: str
    sid: str
    acr: str
    allowed_origins: list[str] = Field(default_factory=list, alias="allowed-origins")
    realm_access: dict[str, list[str]] = Field(default_factory=dict)
    resource_access: dict[str, dict[str, list[str]]] = Field(default_factory=dict)
    scope: list[str]
    email_verified: bool
    name: str
    preferred_username: str
    given_name: str
    family_name: str
    email: str

    @field_validator('scope', mode="before")
    @classmethod
    def str_to_list(cls, v: str) -> str:
        return v.split()
    
    def can_edit(self) -> bool:
        return self._has_role("role::app_writter", only_this_party=True)
    
    def can_read(self) -> bool:
        return self._has_role("role::app_reader", only_this_party=True)
    
    def _has_role(self, role_name: str, only_this_party: bool = True):
        if only_this_party:
            if self.azp not in self.resource_access:
                return False
            
            all_roles = self.resource_access[self.azp].get("roles", [])
        else:
            all_roles = []
            for value in self.resource_access.values():
                all_roles += value.get("roles", [])
        
        for role in all_roles:
            if role == role_name:
                return True
        return False
    