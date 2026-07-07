from django import forms
from .models import (
    Universidad, Campus, Carrera, MallaCurricular, UnidadCurricular,
    PeriodoDeNivelacion, Paralelo, Horario, CohorteDeMatricula,
    MatriculaParalelo, ConsolidadoAcademico, EvaluacionAcademica,
    IncidenciaAcademica, EvaluacionDeDesempeno, InformeGeneral
)
from poo.clases.carrera import Carrera as CarreraBase



# ══════════════════════════════════════════════════════════════
# BASE
# ══════════════════════════════════════════════════════════════

class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input-estilo'})
            
            


# ══════════════════════════════════════════════════════════════
# UNIVERSIDAD
# ══════════════════════════════════════════════════════════════

class FormularioUniversidad(BaseModelForm):
    class Meta:
        model = Universidad
        fields = ("nombre", "abreviatura", "codigo_sniese", "direccion_matriz", "identificador_visual")
        labels = {
            "nombre": "Nombre de la institución",
            "abreviatura": "Abreviatura",
            "codigo_sniese": "Código SNIESE",
            "direccion_matriz": "Dirección de matriz",
            "identificador_visual": "Identificador visual",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nombre'].required = False
        self.fields['abreviatura'].required = False
        self.fields['codigo_sniese'].required = False
        self.fields['direccion_matriz'].required = False
        self.fields['identificador_visual'].required = False

    def clean(self):
        from poo.clases.universidad import Universidad as UniversidadBase

        cleaned_data = super().clean()

        universidad_poo = UniversidadBase(
            nombre=cleaned_data.get("nombre", ""),
            abreviatura=cleaned_data.get("abreviatura", ""),
            codigo_sniese=cleaned_data.get("codigo_sniese", ""),
            direccion_matriz=cleaned_data.get("direccion_matriz", ""),
        )

        errores = universidad_poo.validar_datos_de_registro()
        if errores:
            raise forms.ValidationError(errores)

        codigo_sniese = (cleaned_data.get("codigo_sniese") or "").strip()
        if codigo_sniese:
            existentes = Universidad.objects.filter(codigo_sniese__iexact=codigo_sniese)
            if self.instance and self.instance.pk:
                existentes = existentes.exclude(pk=self.instance.pk)
            if existentes.exists():
                raise forms.ValidationError(
                    {"codigo_sniese": "La Institución ya ha sido registrada"}
                )

        return cleaned_data






# ══════════════════════════════════════════════════════════════
# CAMPUS
# ══════════════════════════════════════════════════════════════

class FormularioCampus(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ("codigo_de_campus", "nombre", "direccion_fisica", "provincia")
        labels = {
            "codigo_de_campus": "Código de Campus",
            "nombre": "Nombre",
            "direccion_fisica": "Dirección física",
            "provincia": "Provincia",
        }

    def __init__(self, *args, universidad=None, **kwargs):
        self.universidad = universidad
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = False
        self.fields['direccion_fisica'].required = False
        self.fields['provincia'].required = False

        self.fields['codigo_de_campus'].required = False
        self.fields['codigo_de_campus'].widget.attrs.update({
            'placeholder': 'El código será determinado de forma automática',
            'style': 'background-color: #f5f5f7; color: #86868b; pointer-events: none;',
            'readonly': True
        })

    def clean(self):
        from poo.clases.campus import Campus as CampusBase

        cleaned_data = super().clean()

        campus_poo = CampusBase(
            codigo_de_campus=cleaned_data.get("codigo_de_campus", ""),
            nombre=cleaned_data.get("nombre", ""),
            direccion_fisica=cleaned_data.get("direccion_fisica", ""),
            provincia=cleaned_data.get("provincia", ""),
        )

        errores = campus_poo.validar_datos_de_registro()
        if errores:
            raise forms.ValidationError(errores)

        nombre = (cleaned_data.get("nombre") or "").strip()
        if nombre and self.universidad is not None:
            existentes = Campus.objects.filter(universidad=self.universidad, nombre__iexact=nombre)
            if self.instance and self.instance.pk:
                existentes = existentes.exclude(pk=self.instance.pk)
            if existentes.exists():
                raise forms.ValidationError(
                    {"El Campus ya ha sido registrado"}
                )

        return cleaned_data




# ══════════════════════════════════════════════════════════════
# CARRERA
# ══════════════════════════════════════════════════════════════

class FormularioCarrera(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ("campus", "codigo_de_carrera", "nombre", "vigencia_sniese")
        labels = {
            "campus": "Campus registrado",
            "codigo_de_carrera": "Código de Carrera",
            "nombre": "Nombre",
            "vigencia_sniese": "Vigencia SNIESE",
        }
        widgets = {
            "vigencia_sniese": forms.DateInput(attrs={"type": "date"}, format='%Y-%m-%d'),
            "codigo_de_carrera": forms.TextInput(attrs={
                'placeholder': 'El código será determinado de forma automática', 
                'style': 'background-color: #f5f5f7; color: #86868b; pointer-events: none;', 
                'readonly': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campus'].required = False
        self.fields['nombre'].required = False
        self.fields['vigencia_sniese'].required = False
        self.fields['codigo_de_carrera'].required = False
        if self.instance and self.instance.pk and self.instance.vigencia_sniese:
            self.fields['vigencia_sniese'].widget.attrs['value'] = self.instance.vigencia_sniese.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        
        campus = cleaned_data.get("campus")
        nombre = cleaned_data.get("nombre")
        vigencia_sniese = cleaned_data.get("vigencia_sniese")

        errores = {}

        if not campus: errores['campus'] = "Información requerida"
        if not nombre: errores['nombre'] = "Información requerida"
        if not vigencia_sniese: errores['vigencia_sniese'] = "Información requerida"

        if nombre and vigencia_sniese:
            carrera_poo = CarreraBase(
                codigo_de_carrera="PENDIENTE",
                nombre=nombre,
                vigencia_sniese=vigencia_sniese
            )

            errores_poo = carrera_poo.validar_datos_de_registro()
            if errores_poo:
                errores.update(errores_poo)

            if "vigencia_sniese" not in errores and not carrera_poo.esta_activa():
                errores['vigencia_sniese'] = "La vigencia SNIESE ha expirado"

        if campus and nombre:
            existentes = Carrera.objects.filter(campus=campus, nombre__iexact=nombre.strip())
            if self.instance and self.instance.pk:
                existentes = existentes.exclude(pk=self.instance.pk)
            if existentes.exists():
                errores['nombre'] = "La Carrera ya ha sido registrada"

        if errores:
            raise forms.ValidationError(errores)

        return cleaned_data