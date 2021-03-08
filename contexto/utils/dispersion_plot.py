# Librerias necesarias
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import warnings


# Objeto dispersionPlot
class dispersionPlot:
    def __init__(self, text, keywords, ignore_case=True,
                 title='Gráfico de dispersión de palabras',
                 label_x='Distribución de términos',
                 label_y='Términos de interés',
                 labels=None,
                 auto_labels=True,
                 figsize=(12, 7),
                 marker='|', marker_size=20, marker_width=3,
                 colors=None, cm='nipy_spectral',
                 legend=True,
                 rotation=30,
                 show=True,
                 outpath=None,
                 return_fig=False
                 ):
        self._ignore_case = ignore_case
        self.textos = text
        self.keywords = keywords
        self._title = title
        self._label_x = label_x
        self._label_y = label_y
        self._autolabels = auto_labels
        self.labels = labels
        self._marker = marker
        self._marker_size = marker_size
        self._marker_width = marker_width
        self._cm = cm
        self.colors = colors
        self._rotation = rotation
        self._legend = legend
        self._show = show
        self._outpath = outpath
        self._figsize = figsize
        self._return_fig = return_fig
        self._set_limites_x()
        self._calcular_dispersion()

    @property
    def textos(self):
        return self._textos

    @textos.setter
    def textos(self, text):
        if isinstance(text, str):
            self._textos = [text]
            all_words = self._textos.split()
        elif isinstance(text, list):
            self._textos = text
            all_words = ' '.join(self._textos).split()
        else:
            raise ValueError(
                'Tipo de datos desconocido, por favor ingrese un texto o una lista de textos')

        if self._ignore_case:
            self._all_words = list(map(str.lower, all_words))
        else:
            self._all_words = all_words

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        if isinstance(keywords, list):
            if self._ignore_case:
                keywords = list(map(str.lower, keywords))

            if len(np.unique(keywords)) != len(keywords):
                warnings.warn(
                    'Existen palabras clave repetidas. Estás serán eliminadas')
                indexes = np.unique(keywords, return_index=True)[1]
                keywords = [keywords[index] for index in sorted(indexes)]
                keywords.reverse()
            self._comprobar_existencia(keywords)

        else:
            raise ValueError(
                'Por favor ingrese una lista términos o palabras clave')

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels):
        if labels is None and self._autolabels:
            self._labels = [f'Doc {i+1}' for i in range(len(self.textos))]
        elif labels is None:
            self._labels = None
        elif isinstance(labels, list):
            if len(labels) == len(self.textos):
                self._labels = labels
            else:
                raise ValueError(
                    'El número de etiquetas de entrada no es igual al número de documentos.')
        else:
            raise ValueError(
                'El tipo de datos de las etiquetas no está permitido, por favor ingrese una lista de etiquetas.')

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors):
        if colors is None:
            self._colors = self._paleta_color()
        elif isinstance(colors, list):
            if len(colors) == len(self.textos):
                self._colors = colors
            else:
                raise ValueError(
                    'El número de colores de entrada debe ser igual al número de documentos')
        else:
            raise ValueError(
                'Tipo de datos en colores es desconocido, por favor ingrese una lista de colores.')

    def _set_limites_x(self):
        """
        Función para calcular finales de documentos y posición de etiquetas en plot
        """
        limits = [len(t.split()) for t in self._textos]
        limits = np.cumsum(limits) - 1
        limits_ = np.insert(limits, 0, 0)
        x_pos = [limits_[i] + (limits_[i + 1] - limits_[i]) /
                 2 for i in range(len(limits))]
        self._limits = limits
        self._x_limits = x_pos

    def _comprobar_existencia(self, keywords):
        """
        Comprueba si las keywords de entrada están en le texto.
        """
        no_words = [w for w in keywords if w not in self._all_words]
        if no_words:
            if len(no_words) == len(keywords):
                raise ValueError(
                    'No existe ninguna palabra clave asociada a los documentos.')
            warnings.warn(
                'Advertencia: las palabras: ({}) no están en los documentos de entrada'.format(
                    ', '.join(no_words)))
            self._keywords = [w for w in keywords if w not in no_words]
        else:
            self._keywords = keywords

    def _paleta_color(self):
        """
        Define automaticamente los colores si colors=None
        """
        cmap = cm.get_cmap(self._cm)
        niveles = len(self._textos)
        colores = [cmap(c / (2 * niveles)) if c %
                   2 else cmap(0.5 + c / (2 * niveles)) for c in range(niveles)]
        return colores

    def _calcular_dispersion(self):
        """
        Calcula la dispersión de los términos en los documentos
        """
        points = [
            (x, y)
            for x in range(len(self._all_words))
            for y in range(len(self.keywords))
            if self._all_words[x] == self.keywords[y]
        ]

        x, y = list(zip(*points))
        self._points_x = x
        self._points_y = y

    def graficar(self):
        """
        Función para graficar la dispersión.
        """
        x = np.asarray(self._points_x)
        y = np.asarray(self._points_y)
        fig, ax = plt.subplots(figsize=self._figsize)
        lines = list()

        for i, d in enumerate(self._limits):
            if i == 0:
                lines += ax.plot(
                    x[(x >= 0) & (x <= d)],
                    y[(x >= 0) & (x <= d)],
                    self._marker,
                    ms=self._marker_size,
                    mew=self._marker_width,
                    color=self.colors[i])

            else:
                d_ant = self._limits[i - 1]
                lines += ax.plot(
                    x[(x > d_ant) & (x <= d)],
                    y[(x > d_ant) & (x <= d)],
                    self._marker,
                    ms=self._marker_size,
                    mew=self._marker_width,
                    color=self._colors[i])

            ax.axvline(x=d + 0.5, color='lightgray',
                       linestyle='dashed')

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
        ax.set_title(self._title, {'fontsize': 15, 'fontweight': 700})
        ax.set_xlabel(self._label_x)
        ax.set_xlim(0.2, x[-1] + 0.2)
        ax.set_xticks(self._x_limits)
        if self._labels is not None:
            ax.set_xticklabels(self._labels, rotation=self._rotation)
            if self._legend:
                ax.legend(lines, self._labels, bbox_to_anchor=(1.003, 1),
                          loc='upper left', markerscale=0.5, frameon=False)
        ax.set_ylabel(self._label_y)
        ax.set_yticks(list(range(len(self.keywords))))
        ax.set_yticklabels(self._keywords)

        if self._outpath is not None:
            plt.savefig(self._outpath, bbox_inches='tight',
                        transparent=False, facecolor='w', dpi=300)
        if self._show:
            plt.show()
        if not self._show and self._outpath is None:
            warnings.warn(
                'por favor fije un directorio para guardar la imagen')
            plt.show()
        if self.return_fig:
            return fig
        return ax
