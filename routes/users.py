from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from jwt import PyJWTError

from common.const import ACCESS_TOKEN_EXPIRE_MINUTES
from models.users import UserSignup, UserSignin, UpdateProfile  # Adjust import path as necessary
from helpers.users import add_user, find_user, update_user  # Adjust import path as necessary
from tools.jwt import create_access_token, verify_token
from tools.pwd import hash_password, verify_password

router = APIRouter()


@router.post("/signup/")
async def signup(user: UserSignup):
    existing_user = await find_user(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        hashed_password = hash_password(user.password)  # Hash the password
        user.password = hashed_password  # Replace the plain password with the hashed one
        new_user = await add_user(user.dict())

        # Generate JWT token for the new user
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        # Return the access token along with the new user info
        # Adjust the returned user info as necessary
        return {"user": {"username": new_user["username"], "email": new_user["email"]},
                "access_token": access_token,
                "token_type": "bearer"}
    except PyJWTError:
        raise HTTPException(status_code=500, detail="Could not generate access token")
    except Exception as e:
        # Log the exception details here with logging library of your choice
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred during sign up")


@router.post("/signin/")
async def signin(user: UserSignin):
    try:
        existing_user = await find_user(user.username)

        if not existing_user or not verify_password(user.password, existing_user['password']):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except PyJWTError:
        raise HTTPException(status_code=500, detail="Could not generate access token")
    except Exception as e:
        # Log the exception details here with logging library of your choice
        raise HTTPException(status_code=500, detail="An error occurred during sign in")


@router.put("/update-profile/{username}")
async def update_profile(username: str, user: UpdateProfile, payload: dict = Depends(verify_token)):
    # Ensure the user updating the profile is the same as the logged-in user
    if payload.get("sub") != username:
        raise HTTPException(status_code=403, detail="Not authorized to update this user's profile")

    updated_user = await update_user(username, user.dict())
    if updated_user:
        return {"message": "User profile updated successfully"}
    else:
        return {"message": "No update was made"}
