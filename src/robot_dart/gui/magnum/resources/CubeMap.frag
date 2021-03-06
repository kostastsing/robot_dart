in highp vec4 worldPosition;

#ifdef EXPLICIT_UNIFORM_LOCATION
layout(location = 1)
#endif
uniform highp vec3 lightPosition;

#ifdef EXPLICIT_UNIFORM_LOCATION
layout(location = 2)
#endif
uniform highp float farPlane;

#ifdef TEXTURED
#ifdef EXPLICIT_TEXTURE_LAYER
layout(binding = 1)
#endif
uniform lowp sampler2D diffuseTexture;
#endif

#ifdef EXPLICIT_UNIFORM_LOCATION
layout(location = 4)
#endif
uniform lowp vec4 diffuseColor
    #if !defined(GL_ES) && defined(TEXTURED)
    = vec4(1.0)
    #endif
    ;

#if defined(TEXTURED)
in mediump vec2 interpolatedTextureCoords;
#endif

// layout(location = 0) out float depth;

void main()
{
    lowp vec4 finalDiffuseColor =
        #ifdef TEXTURED
        texture(diffuseTexture, interpolatedTextureCoords)*
        #endif
        diffuseColor;

    /* Ignore transparent pixels */
    if(finalDiffuseColor.a < 1.)
        discard;
    // get distance between object and light source
    float lightDistance = length(worldPosition.xyz - lightPosition);

    // map to [0;1] range by dividing by far_plane
    lightDistance = lightDistance / farPlane;

    // write this as modified depth
    gl_FragDepth = lightDistance;
}